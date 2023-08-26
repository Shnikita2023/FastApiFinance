from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from .shemas import TransactionCreate, TransactionGet
from ..auth.base import current_user
from ..depends.dependencies import UOWDep
from ..transaction.services import TransactionService
from ..users.models import User

router_transaction = APIRouter(
    prefix="/transaction",
    tags=["transactions"]
)


@router_transaction.post(path="/", summary='Добавление транзакции')
async def create_transaction(uow: UOWDep,
                             new_transaction: TransactionCreate,
                             user: User = Depends(current_user)) -> dict:
    try:
        transaction_id: int = await TransactionService().add_transaction(new_transaction, uow)

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


@router_transaction.get(path="/all", summary='Получение всех транзакций пользователя', response_model=list[TransactionGet])
@cache(expire=600)
async def get_all_transactions(uow: UOWDep,
                               user: User = Depends(current_user),
                               value: Optional[int] = None,
                               param_column: str = "user_id") -> list[TransactionGet]:
    try:
        if value is None:
            value: int = user.id
        all_transactions: list[TransactionGet] = await TransactionService().get_transaction_by_param(value, uow,
                                                                                                     param_column)
        return all_transactions

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение всех транзакций"
        })


@router_transaction.get(path="/{transaction_id}", summary='Получение транзакции пользователя по id',
                        response_model=TransactionGet)
async def get_one_transaction(uow: UOWDep,
                              transaction_id: int,
                              user: User = Depends(current_user)) -> TransactionGet:
    try:
        one_transaction: TransactionGet = await TransactionService().get_transaction(transaction_id, uow)
        return one_transaction

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение транзакции"
        })


@router_transaction.delete(path="/{transaction_id}", summary='Удаление транзакции пользователя')
async def delete_transaction(uow: UOWDep,
                             transaction_id: int,
                             user: User = Depends(current_user)) -> dict:
    try:
        one_transaction: int = await TransactionService().delete_transaction(transaction_id, uow)
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
