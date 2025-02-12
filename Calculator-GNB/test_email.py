import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SMTP_EMAIL = "talgat707@mail.ru"
SMTP_PASSWORD = "bugDMbgb9kzMHnyjYtNm"
RECEIVER_EMAIL = "talgat707@mail.ru"

subject = "Тестовое письмо"
body = "Это тестовое письмо для проверки SMTP."

msg = MIMEMultipart()
msg["From"] = SMTP_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("✅ Письмо отправлено!")
except Exception as e:
    print(f"❌ Ошибка отправки email: {e}")

