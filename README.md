# Calculator-GNB

Калькулятор предварительной стоимости ГНБ (горизонтально направленного бурения).
Клиент вводит длину и диаметр, видит цену, заявка уходит на email.

## Структура
- `server.py` — Flask-сервер: отдаёт страницу и шлёт заявки на почту (`/submit`).
- `static/` — фронтенд: `index.html`, `script.js` (расчёт), `styles.css`.

## Переменные окружения
- `SMTP_EMAIL` — почта-отправитель (mail.ru)
- `SMTP_PASSWORD` — пароль приложения mail.ru
- `AIRTABLE_TOKEN` — токен Airtable (scope `data.records:write`, доступ к базе «Заявки ГНБ»). Без него заявки идут только на почту.

Заявка считается принятой, если сработал хотя бы один канал: почта или Airtable.

Пароли в код не писать — только через переменные окружения (Render → Environment).

## Запуск локально
```bash
pip install -r requirements.txt
SMTP_EMAIL=... SMTP_PASSWORD=... python server.py   # http://localhost:10000
```
Прод: `gunicorn server:app`
