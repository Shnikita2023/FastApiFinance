from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


from .models import Expense
from .shemas import ExpenseCreate
from ..auth.base import current_user
from ..category.models import Category
from ..category.router import router_categories, get_category
from ..users import User
from app.db.database import get_async_session


router_expenses = APIRouter(
    prefix="/expense",
    tags=["Expenses"]
)


@router_expenses.post("/add", summary='Добавление расходов')
async def add_expenses(new_expense: ExpenseCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Expense).values(**new_expense.dict())
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "succeses",
            "data": f"expense added",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_expenses.post("/", summary='Формирование финансов(дох/рас)')
async def formation_expenses(data_form: dict, user: User = Depends(current_user),
                             category: Category = Depends(get_category)):
    try:
        expenses_data = ExpenseCreate(
            amount=data_form["amount"],
            description=data_form["description"],
            user_id=user.id,
            category_id=category.id,
        )
        async with AsyncClient() as client:
            URL = "http://localhost:8000/"
            if data_form["type"] == "Расход":
                slug = "expense/add"
            else:
                slug = "income/add"

            response = await client.post(f"{URL}{slug}", json=expenses_data.dict())

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
