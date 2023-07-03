import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST
from app.db.database import get_async_session, Base
from app.main import app

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = get_async_session_test


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client

@pytest.fixture(scope="session")
def user_token() -> dict:
    # Создание пользователя, авторизация и получение токена
    data = {
        "email": "usertest@mail.ru",
        "password": "userpass",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Nikita",
        "last_name": "Ivanov",
        "first_name": "Никита"
    }
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201, f"Ошибка при создании пользователя: {response.text}"

    data = {
        "username": "usertest@mail.ru",
        "password": "userpass",
    }
    response = client.post("/auth/jwt/login", data=data)
    assert response.status_code == 200 or 204, f"Ошибка авторизации: {response.text}"

    cookie = response.headers["set-cookie"].split(";")[0]
    return {"Cookie": cookie}
