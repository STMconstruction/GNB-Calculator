from flask import Flask, request, jsonify
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder="", static_url_path="")

# Настройки SMTP
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SMTP_EMAIL = "talgat707@mail.ru"
SMTP_PASSWORD = "bugDMbgb9kzMHnyjYtNm"  # Замените на ваш пароль приложения
RECEIVER_EMAIL = "talgat707@mail.ru"

# Функция отправки email
def send_email(data):
    try:
        subject = "📩 Новая заявка от клиента!"
        body = f"""\
Имя: {data['name']}
Телефон: {data['phone']}
Длина бурения: {data['length']} м
Диаметр трубы: {data['diameter']} мм
Примерная стоимость: {data['cost']} тенге
"""
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        print("✅ Заявка отправлена на email!")
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")

# Маршрут для отправки заявок
@app.route("/submit", methods=["POST"])
def submit_request():
    try:
        client_data = request.json
        print("Полученные данные:", client_data)

        # Сохраняем заявку в файл
        with open("clients.json", "a", encoding="utf-8") as f:
            json.dump(client_data, f, ensure_ascii=False)
            f.write("\n")

        # Отправляем email
        send_email(client_data)

        return jsonify({"success": True})
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/")
def index():

    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

