from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from .shemas import TransactionCreate, TransactionGet
from ..auth.base import current_user
from ..balance.models import Balance
from ..balance.router import get_balance_by_param
from ..category.models import Category
from ..category.router import get_item_by_param
from ..balance.services import BalanceService
from ..depends.dependencies import UOWDep
from ..transaction.services import TransactionService
from ..users.models import User


router_transaction = APIRouter(
    prefix="/transaction",
    tags=["transactions"]
)


@router_transaction.post("/add", summary='Добавление транзакции')
async def create_transaction(uow: UOWDep,
                             data_form: dict,
                             category: Category = Depends(get_item_by_param),
                             user: User = Depends(current_user)) -> dict:
    try:
        balance = await BalanceService().get_balance_by_param(value=user.id, uow=uow)
        new_transaction = TransactionCreate(
            comment=data_form["comment"],
            amount=data_form["amount"],
            type_transaction=data_form["type_transaction"],
            user_id=user.id,
            category_id=category.id,
            balance_id=balance.id
        )
        transaction_id = await TransactionService().add_transaction(new_transaction, uow)

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
async def get_transactions(uow: UOWDep,
                           user: User = Depends(current_user),
                           value: Optional[int] = None,
                           param_column: str = "user_id"):
    try:
        if value is None:
            value = user.id
        all_transactions = await TransactionService().get_transaction_by_param(value, uow, param_column)
        return all_transactions

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_transaction.delete("/", summary='Удаление транзакций пользователя')
async def delete_transaction(uow: UOWDep,
                             transaction_id: int,
                             user: User = Depends(current_user)) -> dict:
    try:
        one_transaction = await TransactionService().delete_transaction(transaction_id, uow)
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
