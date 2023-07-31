import aiosmtplib

from email.message import EmailMessage

from aiosmtplib import SMTPConnectError
from fastapi import HTTPException
from app.config import SMTP_PASSWORD, SMTP_USER, SMTP_PORT, SMTP_HOST


async def connect_smtp(body: str, email: str, subject: str) -> None:
    try:
        async with aiosmtplib.SMTP(SMTP_HOST, SMTP_PORT, use_tls=True) as smtp:
            await smtp.login(SMTP_USER, SMTP_PASSWORD)
            message = EmailMessage()
            message["From"] = SMTP_USER
            message["To"] = email
            message["Subject"] = subject
            message.add_alternative(body, subtype='html')
            await smtp.send_message(message=message)

    except Exception as exc:
        SMTPConnectError(f"Error connecting to {SMTP_HOST} on port {SMTP_PORT}: {exc}")


async def send_password_reset_email(email: str, token: str) -> None:
    try:
        URL = "http://127.0.0.1:8000/authentic/"
        body = f"Для сброса пароля перейдите по ссылке: {URL}reset_password?token={token}"
        subject = "Сброс пароля"
        await connect_smtp(body=body, email=email, subject=subject)

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "Error",
            "data": None,
            "details": "Ошибка отправки письма"
        })


async def send_letter_on_after_register(email: str) -> None:
    try:
        body = ("Регистрация успешно пройдена!\n"
                "Добро пожаловать на платформу 'Управление финансами'!")
        subject = "Регистрация прошла успешно"
        await connect_smtp(body=body, email=email, subject=subject)

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "Error",
            "data": None,
            "details": "Ошибка отправки письма"
        })
