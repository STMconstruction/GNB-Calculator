from flask import Flask, request, jsonify, send_from_directory
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Настройки SMTP (Email)
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SMTP_EMAIL = os.getenv("SMTP_EMAIL")  # Загружаем Email из Render Environment Variables
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Пароль тоже загружаем безопасно
RECEIVER_EMAIL = "talgat707@mail.ru"

MAX_LENGTH = 5000
ALLOWED_DIAMETERS = {100, 200, 315}


def price_per_meter(length, diameter):
    """Тариф за метр, тенге. Должен совпадать с static/script.js."""
    if length < 60:
        return {100: 15000, 200: 17000, 315: 18000}[diameter]
    return {100: 10000, 200: 12000, 315: 13000}[diameter]


def normalize_phone(raw):
    """Возвращает 11 цифр вида 7XXXXXXXXXX или None."""
    digits = re.sub(r"\D", "", str(raw or ""))
    if len(digits) == 11 and digits[0] == "8":
        digits = "7" + digits[1:]
    if len(digits) == 11 and digits.startswith("77"):
        return digits
    return None


def format_phone(d):
    return f"+7 ({d[1:4]}) {d[4:7]}-{d[7:9]}-{d[9:11]}"


@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# 📩 Маршрут для обработки формы и отправки email
@app.route("/submit", methods=["POST"])
def submit_request():
    data = request.get_json(silent=True) or {}

    # Бот заполнил скрытое поле — делаем вид, что всё ок, письмо не шлём
    if data.get("website"):
        return jsonify({"success": True})

    name = str(data.get("name") or "").strip()[:60]
    phone = normalize_phone(data.get("phone"))
    try:
        length = float(data.get("drill_length"))
        diameter = int(data.get("pipe_diameter"))
    except (TypeError, ValueError):
        length, diameter = 0, 0

    if not name:
        return jsonify({"success": False, "error": "Введите имя."}), 400
    if not phone:
        return jsonify({"success": False, "error": "Некорректный номер телефона."}), 400
    if not (1 <= length <= MAX_LENGTH) or diameter not in ALLOWED_DIAMETERS:
        return jsonify({"success": False, "error": "Некорректные параметры бурения."}), 400

    # Стоимость считаем на сервере, а не берём с клиента
    total_cost = length * price_per_meter(length, diameter)
    wa_link = f"https://wa.me/{phone}"
    cost_text = f"{total_cost:,.0f}".replace(",", " ")

    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = f"Новый расчет ГНБ: {name}, {length:g} м"

        body = (
            f"Имя: {name}\n"
            f"Телефон: {format_phone(phone)}\n"
            f"WhatsApp клиента: {wa_link}\n"
            f"Длина бурения: {length:g} м\n"
            f"Диаметр трубы: до {diameter} мм\n"
            f"Расчетная стоимость: {cost_text} тг.\n"
        )
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print("✅ Email отправлен!")
        return jsonify({"success": True})
    except Exception as e:
        # Подробности — только в лог сервера, клиенту — общее сообщение
        print(f"❌ Ошибка отправки email: {e}")
        return jsonify({"success": False, "error": "Не удалось отправить заявку. Напишите нам в WhatsApp."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
