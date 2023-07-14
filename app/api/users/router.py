from typing import Any

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.api.auth.base import current_user
from app.api.users import User

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
async def register_user(request: Request) -> Any:
    return templates.TemplateResponse("register_user.html", {"request": request})


@router_authentic.get("/", response_class=HTMLResponse, summary="Шаблон аутентификации")
async def get_template_authentic(request: Request) -> Any:
    return templates.TemplateResponse("authentic.html", {"request": request})


@router_authentic.get("/cabinet", response_class=HTMLResponse, summary="Шаблон кабинета авторизованного user")
async def get_template_authentic_user(request: Request, user: User = Depends(current_user)) -> Any:
    return templates.TemplateResponse("cabinet.html", {"request": request})


@router_authentic.get("/cabinet/get_data_user", response_class=HTMLResponse, summary="Шаблон получение данных пользователя")
async def get_data_user(request: Request, user: User = Depends(current_user)) -> Any:
    data_user = {
        "Почта": user.email,
        "Пароль": "***********",
        "Имя": user.first_name,
        "Фамилия": user.last_name,
        "Ваш ник": user.username,
        "Дата регистрации": user.registered_at,
    }
    return templates.TemplateResponse("get_data_user.html", {"request": request, "data_user": data_user})


@router_authentic.get("/me", summary="Получение профиля user")  # Нужна удалить лишнее
async def get_user_me(user: User = Depends(current_user)):
    return user


@router_authentic.get("/reset_password", summary="Форма сброса пароля")
async def reset_pass(request: Request, token: str) -> Any:
    return templates.TemplateResponse("reset_password.html", {"request": request, 'token': token})


@router_authentic.get("/send_email", summary="Отправка email")
async def send_email(request: Request) -> Any:
    return templates.TemplateResponse("email_recovery.html", {"request": request})
