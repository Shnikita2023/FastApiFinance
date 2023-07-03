from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.api.auth.base import fastapi_users, current_user
from app.api.users import User
from app.api.users.shemas import UserCreate
from app.db.database import get_async_session

templates = Jinja2Templates(directory="app/api/templates")

router_register = APIRouter(
    prefix="/register",
    tags=["Regisration"]
)

router_authentic = APIRouter(
    prefix="/authentic",
    tags=["Authentication"]
)


@router_register.get("/", response_class=HTMLResponse, summary="Шаблон регистрации")
async def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router_authentic.get("/", response_class=HTMLResponse, summary="Шаблон аутентификации")
async def get_template_authentic(request: Request):
    return templates.TemplateResponse("authentic.html", {"request": request})


@router_authentic.get("/cabinet", response_class=HTMLResponse, summary="Шаблон кабинета авторизованного user")
async def get_template_authentic_user(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("base_cabinet.html", {"request": request})

@router_authentic.get("/me", summary="Получение профиля user")
async def get_user_me(user: User = Depends(current_user)):
    return user
