from flask import Flask, request, jsonify
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Данные SMTP (Заменил на переменные окружения)
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SMTP_EMAIL = os.getenv("SMTP_EMAIL")  # Используем переменные окружения
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = "talgat707@mail.ru"

def send_email(client_data):
    """Функция для отправки email с заявкой"""
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "Новая заявка от клиента"

    body = f"Имя: {client_data.get('name')}\nEmail: {client_data.get('email')}"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email успешно отправлен!")
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")

# Маршрут для обработки заявок
@app.route("/submit", methods=["POST"])
def submit_request():
    try:
        client_data = request.json
        print(f"📩 Полученные данные: {client_data}")

        # Сохранение заявки в файл (локально)
        with open("clients.json", "a", encoding="utf-8") as f:
            json.dump(client_data, f, ensure_ascii=False)
            f.write("\n")

        # Отправка email
        send_email(client_data)

        return jsonify({"success": True})
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({"success": False, "error": str(e)})

# Главная страница (статичный index.html)
@app.route("/")
def index():
    return "Сервер работает!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

