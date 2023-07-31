from celery import Celery
from fastapi import Request

from starlette.templating import Jinja2Templates

from ..transaction.shemas import TransactionGet
from ..utils.send_letter_on_email import connect_smtp

celery = Celery('tasks', broker='redis://localhost:6379')

templates = Jinja2Templates(directory="app/api/templates")


async def send_email_report_transaction(request: Request, data_transaction: list[TransactionGet], email_user: str):
    # Загрузить HTML шаблон
    template = templates.get_template("report_transactions.html")
    report_html = template.render(request=request, data_transaction=data_transaction)
    await connect_smtp(body=report_html,
                       email=email_user,
                       subject="Отчёт транзакции")
