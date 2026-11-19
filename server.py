from flask import Flask, request, jsonify, send_from_directory
import json
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

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# 📩 Маршрут для обработки формы и отправки email
@app.route("/submit", methods=["POST"])
def submit_request():
    try:
        client_data = request.json
        print(f"📩 Получены данные: {client_data}")

        # Формируем email
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "Новый расчет стоимости ГНБ"

        body = (
            f"Имя: {client_data.get('name')}\n"
            f"Телефон: {client_data.get('phone')}\n"
            f"Длина бурения: {client_data.get('drill_length')} м\n"
            f"Диаметр трубы: {client_data.get('pipe_diameter')} мм\n"
            f"Расчетная стоимость: {client_data.get('total_cost')} тг.\n"
        )
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # Отправка email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print("✅ Email отправлен!")
        return jsonify({"success": True, "message": "Email отправлен!"})
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

