from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.auth.base import fastapi_users
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

@router_register.get("/", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router_register.get("/", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router_authentic.get("/", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("authentic.html", {"request": request})


# HTTP POST маршрут для обработки отправленной формы регистрации
# @router_register.post("/")
# async def register_post(request: Request, user: UserCreate):
#     # Создаем нового пользователя
#     user_db_user = await fastapi_users.create_user(user)
#     # Возвращаем сообщение об успешной регистрации пользователю
#     return templates.TemplateResponse("base.html", {"request": request, "user": user_db_user})

# @router_register.post("/")
# async def register_user(request: Request, email: str = Form(...),
#                         password: str = Form(...), username: str = Form(...), last_name: str = Form(...),
#                         first_name: str = Form(...)):
#     user_data = {
#         "email": email,
#         "password": password,
#         "username": username,
#         "last_name": last_name,
#         "first_name": first_name,
#     }
#     print(user_data)

