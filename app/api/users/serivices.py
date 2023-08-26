from typing import Any, Type

from fastapi_users.models import UP
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from ..balance.models import Balance
from fastapi import HTTPException


class CustomUserDatabase(SQLAlchemyUserDatabase):
    """Создание пользователя и его баланса в базе данных"""
    async def create(self, create_dict: dict[str, Any]) -> UP:
        try:
            user: Type[UP] = self.user_table(**create_dict)
            self.session.add(user)
            await self.session.flush()
            balance: Balance = Balance(users_id=user.id)
            self.session.add(balance)
            await self.session.commit()
            return user

        except Exception as ex:
            raise HTTPException(status_code=500, detail="Ошибка при создание пользователя")
