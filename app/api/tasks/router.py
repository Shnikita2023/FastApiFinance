from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from .tasks import send_email_report_transaction
from ..auth.base import current_user
from app.api.transaction.services import TransactionService
from ..depends.dependencies import UOWDep

router_tasks = APIRouter(prefix="/report",
                         tags=["tasks"])


@router_tasks.get("/transaction", summary="Получить отчёт по транзакциям")
async def get_transaction_report(background_tasks: BackgroundTasks,
                                 request: Request,
                                 uow: UOWDep,
                                 user=Depends(current_user)) -> dict:
    try:
        list_transaction = await TransactionService().get_transaction_by_param(value=user.id, uow=uow)
        # Задача выполняется на фоне FastAPI в event loop'е или в другом треде
        background_tasks.add_task(send_email_report_transaction, request, list_transaction, user.email)
        return {
            "status": 200,
            "data": "Письмо отправлено",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка отправки отчёта на почту, попробуйте позже"
        })
