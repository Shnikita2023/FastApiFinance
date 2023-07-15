from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.base import current_user
from ..balance.models import Balance
from ..transaction.shemas import TransactionCreate
from ..users import User
from app.db.database import get_async_session

router_balance = APIRouter(
    prefix="/balance",
    tags=["balances"]
)

@router_balance.post("/create", summary='Создание баланса пользователя')
async def create_balance_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        balance = {"users_id": user_id, "total_balance": 0}
        stmt = insert(Balance).values(**balance)
        await session.execute(stmt)
        await session.commit()

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка создание баланса"
        })


@router_balance.get("/", summary='Получение баланса')
async def get_data_balance(session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    try:
        query = select(Balance).where(Balance.users_id == user.id)
        result = await session.execute(query)
        return result.scalar_one()

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


async def update_total_balance(new_transaction: TransactionCreate,
                               session: AsyncSession) -> None:
    """Обновление баланса"""
    try:
        total_balance = select(Balance.total_balance).where(Balance.users_id == new_transaction.user_id)
        result = await session.execute(total_balance)
        if new_transaction.type_transaction == 'Доход':
            new_balance = result.scalar_one() + new_transaction.amount
        else:
            new_balance = result.scalar_one() - new_transaction.amount

        update_balance = (update(Balance).where(Balance.id == new_transaction.balance_id).values
                          (total_balance=new_balance, date=datetime.now()))
        await session.execute(update_balance)
        await session.commit()

    except Exception:
        pass
