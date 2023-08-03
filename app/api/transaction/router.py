from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from .shemas import TransactionCreate, TransactionGet
from ..auth.base import current_user
from ..category.models import Category
from ..category.router import get_item_by_param
from ..balance.services import BalanceService
from ..transaction.services import TransactionService
from ..users.models import User
from ..depends.dependencies import transaction_service, balance_service

router_transaction = APIRouter(
    prefix="/transaction",
    tags=["transactions"]
)


@router_transaction.post("/add", summary='Добавление транзакции')
async def create_transaction(transaction_service: Annotated[TransactionService, Depends(transaction_service)],
                             balance_service: Annotated[BalanceService, Depends(balance_service)],
                             data_form: dict,
                             category: Category = Depends(get_item_by_param),
                             user: User = Depends(current_user)) -> dict:
    try:
        balance = await balance_service.get_balance_by_param(value=user.id)
        new_transaction = TransactionCreate(
            comment=data_form["description"],
            amount=data_form["amount"],
            type_transaction=data_form["type"],
            user_id=user.id,
            category_id=category.id,
            balance_id=balance.id
        )
        transaction_id = await transaction_service.add_transaction(new_transaction, balance_service)

        return {
            "status": "successes",
            "data": transaction_id,
            "details": f"transaction {transaction_id} added"
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка добавление транзакции"
        })


@router_transaction.get("/", summary='Получение всех транзакций пользователя', response_model=list[TransactionGet])
@cache(expire=600)
async def get_transactions(transaction_service: Annotated[TransactionService, Depends(transaction_service)],
                           user: User = Depends(current_user),
                           value: Optional[int] = None,
                           param_column: str = "user_id"):
    try:
        if value is None:
            value = user.id
        all_transactions = await transaction_service.get_transaction_by_param(value, param_column)
        return all_transactions

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_transaction.delete("/", summary='Удаление транзакций пользователя')
async def delete_transaction(transaction_service: Annotated[TransactionService, Depends(transaction_service)],
                             transaction_id: int,
                             user: User = Depends(current_user)) -> dict:
    try:
        one_transaction = await transaction_service.delete_transaction(transaction_id)
        return {
            "status": "successes",
            "data": one_transaction,
            "details": f"transaction c id {one_transaction} delete"
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка удаление транзакций"
        })
