from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from .shemas import BalanceGet, BalanceUpdate
from ..auth.base import current_user
from ..balance.services import BalanceService
from ..depends.dependencies import UOWDep
from ..users.models import User

router_balance = APIRouter(
    prefix="/balance",
    tags=["balances"]
)


@router_balance.post("/", summary='Создание баланса пользователя')
async def create_balance_user(uow: UOWDep,
                              user: User = Depends(current_user)) -> dict:
    try:
        balance_user = await BalanceService().get_balance_by_param(value=user.id, uow=uow)
        if balance_user:
            return {
                "status": "error",
                "data": "У данного пользователя уже есть баланс",
                "details": None
            }
        balance_id = await BalanceService().add_balance(user.id, uow)
        return {
            "status": "successes",
            "data": f"Баланс с id {balance_id} added",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка создание баланса"
        })


@router_balance.get("/{balance_id}", summary='Получение баланса пользователя по id', response_model=BalanceGet)
async def get_data_balance(uow: UOWDep,
                           balance_id: int,
                           user: User = Depends(current_user)) -> BalanceGet:
    try:
        one_balance = await BalanceService().get_balance(balance_id, uow)
        return one_balance

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение баланса"
        })


@router_balance.get("/", summary='Получение баланса пользователя по любым параметрам',
                    response_model=BalanceGet)
async def get_balance_by_param(uow: UOWDep,
                               value: Optional[int] = None,
                               param_column: str = "users_id",
                               user: User = Depends(current_user)):
    try:
        if value is None:
            value = user.id
        one_balance = await BalanceService().get_balance_by_param(value, uow, param_column)
        return one_balance

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение баланса"
        })


@router_balance.patch("/{balance_id}", summary='Обновление баланса пользователя по id')
async def update_total_balance(balance_id: int,
                               new_data: BalanceUpdate,
                               uow: UOWDep,
                               user: User = Depends(current_user)) -> dict:
    try:
        new_balance = await BalanceService().update_balance(balance_id, new_data.total_balance, uow)
        return new_balance

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка обновление баланса"
        })


@router_balance.delete("/{balance_id}", summary='Удаление баланса пользователя по id')
async def delete_balance(balance_id: int,
                         uow: UOWDep,
                         user: User = Depends(current_user)) -> dict:
    try:
        id_balance = await BalanceService().delete_balance(balance_id, uow)
        return {
            "status": "successes",
            "data": f"Баланс с id {id_balance} remove",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка обновление баланса"
        })
