import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.config import REDIS_HOST, REDIS_PORT
from .api.auth.base import fastapi_users, auth_backend
from .api.balance.router import router_balance
from .api.category.router import router_categories
from .api.tasks.router import router_tasks
from .api.transaction.router import router_transaction
from .api.users.router import router_register, router_authentic
from .api.users.shemas import UserRead, UserUpdate, UserCreate

app = FastAPI()

# Подключение статичных файлов
app.mount("/static", StaticFiles(directory="app/api/static"), name="static")

templates = Jinja2Templates(directory="app/api/templates")


@app.get("/base", response_class=HTMLResponse, summary="Начальная страница")
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

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(router_categories)
app.include_router(router_register)
app.include_router(router_authentic)
app.include_router(router_balance)
app.include_router(router_transaction)
app.include_router(router_tasks)

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


@app.on_event("startup")
async def startup() -> None:
    """Подключение редиса при старте"""
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(app)
