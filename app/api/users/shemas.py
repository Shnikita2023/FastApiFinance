import re
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from fastapi_users import schemas
from pydantic import BaseSettings, validator, Field, EmailStr

PATTERN = r"^[А-ЯЁ][а-яё]+$|^[A-Z][a-z]+$"


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str = Field(example="test@mail.ru")
    username: str
    last_name: str
    first_name: str
    registered_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    last_name: str
    first_name: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @validator("password")
    def check_password(cls, password: str) -> str:
        # Проверка на длину пароля
        if len(password) < 8 or len(password) > 50:
            raise HTTPException(status_code=400, detail="Пароль должен быть от 8 до 50 символов")

        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(c.isupper() for c in password):
            raise HTTPException(status_code=400, detail="В пароли должна быть хотя бы одна заглавная буква")

        # Проверка на наличие хотя бы одной строчной буквы
        if not any(c.islower() for c in password):
            raise HTTPException(status_code=400, detail="В пароли должна быть хотя бы одна строчная буква")

        # Проверка на наличие хотя бы одной цифры
        if not any(c.isdigit() for c in password):
            raise HTTPException(status_code=400, detail="В пароли должна быть хотя бы одна цифра")

        # Проверка на наличие хотя бы одного специального символа
        if not re.search(r'[!@#$%^&*()\-_=+{};:,<.>|\[\]\\\/?]', password):
            raise HTTPException(status_code=400,
                                detail="В пароли должен быть хотя бы один символ: !@#$%^&*{}()\-_=+;:,<.>|\[\]\\\/?")

        return password

    @validator("first_name")
    def check_last_name(cls, first_name):
        if not re.match(PATTERN, first_name):
            raise HTTPException(status_code=400,
                                detail="Поля с именем должно быть ru/en и начинаться с большой буквы, затем строчные")
        return first_name


class UserUpdate(UserCreate):
    pass
