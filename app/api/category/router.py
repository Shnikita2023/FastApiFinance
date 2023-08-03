from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_cache.decorator import cache
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from .shemas import CategoryGet, CategoryCreate
from ..auth.base import current_user
from app.api.category.services import CategoryService
from ..users.models import User
from ..depends.dependencies import category_service

templates = Jinja2Templates(directory="app/api/templates")

router_categories = APIRouter(
    prefix="/category",
    tags=["Categories"]
)


@router_categories.get("/get/{id_category}", summary='Получение категории по id', response_model=CategoryGet)
@cache(expire=60)
async def get_category(id_category: int,
                       category_service: Annotated[CategoryService, Depends(category_service)],
                       user: User = Depends(current_user)):
    try:
        one_category = await category_service.get_category(id_category)
        return one_category

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение категории"
        })


@router_categories.get("/", summary='Получение категории по любым параметрам', response_model=CategoryGet)
async def get_item_by_param(value: Any,
                            category_service: Annotated[CategoryService, Depends(category_service)],
                            param_column: str = "name",
                            user: User = Depends(current_user)):
    try:
        one_category = await category_service.get_category_by_param(param_column, value)
        return one_category

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение категории"
        })


@router_categories.get("/all", summary='Получение списка всех категорий', response_model=list[CategoryGet])
async def get_all_categories(category_service: Annotated[CategoryService, Depends(category_service)],
                             user: User = Depends(current_user)):
    try:
        all_category = await category_service.get_categories()
        return all_category

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка получение всех категорий"
        })


@router_categories.post("/add", summary='Добавление категории')
async def create_category(new_categorie: CategoryCreate,
                          category_service: Annotated[CategoryService, Depends(category_service)],
                          user: User = Depends(current_user)):
    try:
        category_id = await category_service.add_category(new_categorie)
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
                          category_service: Annotated[CategoryService, Depends(category_service)]) -> dict:
    try:
        await category_service.delete_category(category_id)
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
