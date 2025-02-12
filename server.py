from flask import Flask, request, jsonify, send_from_directory
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__, static_folder="static")

# SMTP настройки
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = "talgat707@mail.ru"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/submit", methods=["POST"])
def submit_request():
    try:
        client_data = request.json
        print(f"📩 Получены данные: {client_data}")

        # Сохранение данных в файл
        with open("clients.json", "a", encoding="utf-8") as f:
            json.dump(client_data, f, ensure_ascii=False)
            f.write("\n")

        # Отправка email
        send_email(client_data)

        return jsonify({"success": True, "message": "Email отправлен!"})
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({"success": False, "error": str(e)})

def send_email(client_data):
    """Функция отправки email"""
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "Новая заявка от клиента"

    body = f"""
    📩 Новая заявка:
    Имя: {client_data.get('name')}
    Телефон: {client_data.get('phone')}
    Длина бурения: {client_data.get('drill_length')} м
    Диаметр трубы: {client_data.get('pipe_diameter')} мм
    💰 Итоговая стоимость: {client_data.get('total_cost')} ₽
    """
    
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        print(f"📨 Отправка email на {RECEIVER_EMAIL}...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email успешно отправлен!")
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

