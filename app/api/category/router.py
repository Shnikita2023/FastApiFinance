from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_cache.decorator import cache
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from .shemas import CategoryGet, CategoryCreate
from ..auth.base import current_user
from app.api.category.services import CategoryService
from ..depends.dependencies import UOWDep
from ..users.models import User


templates = Jinja2Templates(directory="app/api/templates")

router_categories = APIRouter(
    prefix="/category",
    tags=["Categories"]
)


@router_categories.get("/{id_category}", summary='Получение категории по id', response_model=CategoryGet)
@cache(expire=60)
async def get_category(id_category: int,
                       uow: UOWDep,
                       user: User = Depends(current_user)) -> CategoryGet:
    try:
        one_category: CategoryGet = await CategoryService().get_category(id_category, uow)
        return one_category

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение категории"
        })


@router_categories.get("/", summary='Получение категории по любым параметрам', response_model=CategoryGet)
async def get_item_by_param(value: Any,
                            uow: UOWDep,
                            param_column: str = "name",
                            user: User = Depends(current_user)) -> CategoryGet:
    try:
        one_category: CategoryGet = await CategoryService().get_category_by_param(param_column, value, uow)
        return one_category

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение категории"
        })


@router_categories.get("/all", summary='Получение списка всех категорий', response_model=list[CategoryGet])
async def get_all_categories(uow: UOWDep,
                             user: User = Depends(current_user)) -> list[CategoryGet]:
    try:
        all_category: list[CategoryGet] = await CategoryService().get_categories(uow)
        return all_category

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение всех категорий"
        })


@router_categories.post("/", summary='Добавление категории')
async def create_category(new_categorie: CategoryCreate,
                          uow: UOWDep,
                          user: User = Depends(current_user)) -> dict:
    try:
        category_id: int = await CategoryService().add_category(new_categorie, uow)
        return {
            "status": "successes",
            "data": f"product с номером {category_id} added",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка добавление категории"
        })


@router_categories.delete("/", summary='Удаление категории')
async def delete_category(category_id: int,
                          uow: UOWDep) -> dict:
    try:
        await CategoryService().delete_category(category_id, uow)
        return {
            "status": "successes",
            "data": f"product c id {category_id} removed",
            "details": None
        }

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка удаление категории"
        })


@router_categories.get("/add_category", response_class=HTMLResponse, summary="Шаблон для добавление категорий")
async def add_category(request: Request,
                       user: User = Depends(current_user)):
    return templates.TemplateResponse("category.html", {"request": request})
