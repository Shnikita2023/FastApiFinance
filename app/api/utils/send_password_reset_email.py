import aiosmtplib

from email.message import EmailMessage
from fastapi import HTTPException
from app.config import SMTP_PASSWORD, SMTP_USER, SMTP_PORT, SMTP_HOST


async def send_password_reset_email(email: str, token: str) -> None:
    try:
        async with aiosmtplib.SMTP(SMTP_HOST, SMTP_PORT, use_tls=True) as smtp:
            await smtp.login(SMTP_USER, SMTP_PASSWORD)
            URL = "http://127.0.0.1:8000/authentic/"
            body = f"Для сброса пароля перейдите по ссылке: {URL}reset_password?token={token}"
            message = EmailMessage()
            message["From"] = SMTP_USER
            message["To"] = email
            message["Subject"] = "Сброс пароля"
            message.set_content(body)
            await smtp.send_message(message=message)

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "Error",
            "data": None,
            "details": "Ошибка отправки письма"
        })
