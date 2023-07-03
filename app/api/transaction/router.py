from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Transaction
from .shemas import TransactionCreate
from ..auth.base import current_user
from ..balance.models import Balance
from ..balance.router import get_data_balance, update_total_balance
from ..category.models import Category
from ..category.router import get_category
from ..users import User
from app.db.database import get_async_session

router_transaction = APIRouter(
    prefix="/transaction",
    tags=["transactions"]
)


@router_transaction.post("/add", summary='Добавление транзакции')
async def add_transaction(new_transaction: TransactionCreate,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        await update_total_balance(new_transaction, session)
        await add_transaction(session, new_transaction)
        return {
            "status": "succeses",
            "data": f"transaction added",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


async def add_transaction(session: AsyncSession, new_transaction: TransactionCreate):
    add_transaction = insert(Transaction).values(**new_transaction.dict())
    await session.execute(add_transaction)
    await session.commit()


@router_transaction.post("/", summary='Формирование транзакции')
async def formation_transaction(data_form: dict,
                                user: User = Depends(current_user),
                                category: Category = Depends(get_category),
                                balance: Balance = Depends(get_data_balance)):
    try:
        transaction_data = TransactionCreate(
            comment=data_form["description"],
            amount=data_form["amount"],
            type_transaction=data_form["type"],
            user_id=user.id,
            category_id=category.id,
            balance_id=balance.id
        )

        async with AsyncClient() as client:
            URL = "http://localhost:8000/transaction/add"
            response = await client.post(f"{URL}", json=transaction_data.dict())

        # Проверяем статус-код ответа
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()


    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


