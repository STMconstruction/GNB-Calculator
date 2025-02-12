лfrom flask import Flask, request, jsonify
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# 🔥 Используем переменные окружения для безопасности
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SMTP_EMAIL = os.getenv("SMTP_EMAIL")  # Загружаем Email из Render Environment Variables
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Пароль тоже загружаем безопасно
RECEIVER_EMAIL = "talgat707@mail.ru"  # Получатель email

def send_email(client_data):
    """Функция отправки email"""
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

# 🌐 Главная страница (Проверка работы сервера)
@app.route("/")
def index():
    return "Сервер работает! 🚀"

# 📩 Маршрут для обработки формы
@app.route("/submit", methods=["POST"])
def submit_request():
    try:
        client_data = request.json  # Получаем данные из запроса
        print(f"📩 Получены данные: {client_data}")

        # Сохранение данных в файл (локально)
        with open("clients.json", "a", encoding="utf-8") as f:
            json.dump(client_data, f, ensure_ascii=False)
            f.write("\n")

        # Отправляем email
        send_email(client_data)

        return jsonify({"success": True, "message": "Email отправлен!"})
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({"success": False, "error": str(e)})

# Запуск сервера на порту 10000 для Render
if __name__ == "__main__":
    app.run(host="0.0.0.0",


