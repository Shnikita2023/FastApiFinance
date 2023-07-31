from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException

from .shemas import BalanceGet, BalanceUpdate
from ..auth.base import current_user
from ..balance.services import BalanceService
from ..users.models import User
from ..depends.dependencies import balance_service

router_balance = APIRouter(
    prefix="/balance",
    tags=["balances"]
)


@router_balance.post("/", summary='Создание баланса пользователя')
async def create_balance_user(balance_service: Annotated[BalanceService, Depends(balance_service)],
                              user: User = Depends(current_user)) -> dict:
    try:
        balance_id = await balance_service.add_balance(user.id)
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


@router_balance.get("/get/{balance_id}", summary='Получение баланса пользователя', response_model=BalanceGet)
async def get_data_balance(balance_service: Annotated[BalanceService, Depends(balance_service)],
                           balance_id: int,
                           user: User = Depends(current_user)) -> BalanceGet:
    try:
        one_balance = await balance_service.get_balance(balance_id)
        return one_balance

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение баланса"
        })


@router_balance.get("/", summary='Получение баланса пользователя по любым параметрам',
                    response_model=BalanceGet)
async def get_balance_by_param(balance_service: Annotated[BalanceService, Depends(balance_service)],
                               value: Optional[int] = None,
                               param_column: str = "users_id",
                               user: User = Depends(current_user)):
    try:
        if value is None:
            value = user.id
        one_balance = await balance_service.get_balance_by_param(value, param_column)
        return one_balance

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение баланса"
        })


@router_balance.patch("/{balance_id}", summary='Обновление баланса пользователя')
async def update_total_balance(balance_id: int,
                               new_data: BalanceUpdate,
                               balance_service: Annotated[BalanceService, Depends(balance_service)],
                               user: User = Depends(current_user)) -> dict:
    try:
        new_balance = await balance_service.update_balance(balance_id, new_data.total_balance)
        return new_balance

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка обновление баланса"
        })
