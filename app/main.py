from fastapi import FastAPI, Depends, Body, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient
from pydantic import BaseModel

from redis import asyncio as aioredis
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.api.auth.base import auth_backend, fastapi_users, current_user
from app.api.category.router import router_categories
from app.api.expenses.router import router_expenses
from app.api.incomes.router import router_incomes
from app.api.users import User
from app.api.users.router import router_register, router_authentic
from app.api.users.shemas import UserRead, UserCreate

app = FastAPI()

# Подключение статичных файлов
app.mount("/static", StaticFiles(directory="app/api/static"), name="static")

templates = Jinja2Templates(directory="app/api/templates")



@app.get("/base", response_class=HTMLResponse)
async def base_menu(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# Регистрация роутеров

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_categories)
app.include_router(router_register)
app.include_router(router_authentic)
app.include_router(router_expenses)
app.include_router(router_incomes)




origins = [
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

# @app.on_event("startup")
# async def startup() -> None:
#     """Подключение редиса при старте"""
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
