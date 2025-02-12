from flask import Flask, request, jsonify, send_from_directory
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# 📌 Создаем приложение Flask и указываем, где хранятся файлы фронтенда
app = Flask(__name__, static_folder="static")

# ✅ 1. Раздача главной страницы (index.html)
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# ✅ 2. Раздача статических файлов (CSS, JS)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# 🔥 3. API-эндпоинт для отправки email
@app.route("/submit", methods=["POST"])
def submit_request():
    try:
        client_data = request.json
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

# ✅ 4. Функция отправки email через Mail.ru SMTP
def send_email(client_data):
    SMTP_SERVER = "smtp.mail.ru"
    SMTP_PORT = 465
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    RECEIVER_EMAIL = "talgat707@mail.ru"

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

# ✅ 5. Запуск сервера на порту 10000 для Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

