from flask import Flask, request, jsonify
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Настройки SMTP (Email)
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = "talgat707@mail.ru"

# 🔍 Проверяем переменные перед запуском
print(f"📌 SMTP_EMAIL: {SMTP_EMAIL}")
print(f"📌 SMTP_PASSWORD: {'✅ Установлен' if SMTP_PASSWORD else '❌ НЕ установлен'}")

# 🌐 Маршрут для проверки работы сервера
@app.route("/")
def index():
    return "Сервер работает! 🚀"

# 📩 Маршрут для обработки формы
@app.route("/submit", methods=["POST"])
def submit_request():
    try:
        client_data = request.json
        print(f"📩 Получены данные: {client_data}")

        # Сохранение данных
        with open("clients.json", "a", encoding="utf-8") as f:
            json.dump(client_data, f, ensure_ascii=False)
            f.write("\n")

        # Отправляем email
        send_email(client_data)

        return jsonify({"success": True, "message": "Email отправлен!"})
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({"success": False, "error": str(e)})

# 📨 Функция отправки email
def send_email(client_data):
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "Новая заявка от клиента"

    body = f"Имя: {client_data.get('name')}\nEmail: {client_data.get('email')}"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        print(f"📨 Отправка email на {RECEIVER_EMAIL}...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email отправлен!")
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")

# 📌 Логируем зарегистрированные маршруты перед запуском сервера
print("✅ Зарегистрированные маршруты Flask:")
for rule in app.url_map.iter_rules():
    print(rule)

# 🔥 Запуск сервера на порту 10000 для Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

