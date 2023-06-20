from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category
from .shemas import CategoryGet, CategoryCreate

from app.db.database import get_async_session
from ..auth.base import current_user
from ..users import User

router_categories = APIRouter(
    prefix="/category",
    tags=["Categories"]
)


@router_categories.get("/", summary='Получение категории', response_model=CategoryGet)
async def get_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.get(Category, category_id)
        return result

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_categories.get("/all", summary='Получение списка всех категорий', response_model=list[CategoryGet])
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Category)
        result = await session.execute(query)
        return result.scalars().all()

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_categories.post("/add", summary='Добавление категории')
async def add_category(new_categorie: CategoryCreate, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    try:
        stmt = insert(Category).values(**new_categorie.dict())
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "succeses",
            "data": f"product {new_categorie.name} added",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router_categories.delete("/{category_id}", summary='Удаление категории')
async def delete_categorie(categorie_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        find_category = await session.get(Category, categorie_id)
        if find_category:
            stmt = delete(Category).where(Category.id == categorie_id)
            await session.execute(stmt)
            await session.commit()
            return {
                "status": "succeses",
                "data": f"product {find_category.name} removed",
                "details": None
            }

        return {"message": "Категория не найдена"}

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
