from typing import Optional, Union, Any

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin, models, schemas

from .utils import get_user_db
from ..users.shemas import UserCreate
from ..users.models import User
from ..utils.send_letter_on_email import send_password_reset_email, send_letter_on_after_register
from app.config import SECRET_AUTH_RESET, SECRET_AUTH_VERIF_TOKEN


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH_RESET
    verification_token_secret = SECRET_AUTH_VERIF_TOKEN

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """Регистрация пользователя"""
        await self.validate_password(user_create.password, user_create)
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise HTTPException(status_code=400,
                                detail="Пользователь с таким email уже зарегистрирован")

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        # Создание пользователя
        created_user = await self.user_db.create(create_dict=user_dict)

        await self.on_after_register(created_user, request)
        return created_user

    async def on_after_register(self, user: models.UP, request: Optional[Request] = None) -> None:
        await send_letter_on_after_register(user.email)

    async def get_by_email(self, user_email: str) -> models.UP:
        user = await self.user_db.get_by_email(user_email)

        if user is None:
            raise HTTPException(status_code=400, detail='Невалидные данные, проверьте корректность ввода')
        return user

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None) -> None:
        await send_password_reset_email(email=user.email, token=token)

    async def validate_password(self, password: str, user: Union[schemas.UC, models.UP]) -> str:
        if UserCreate.check_password(password=password):
            return password
        raise HTTPException(status_code=400, detail="Пароль невалидный")

    async def on_after_reset_password(self, user: User, request: Optional[Request] = None) -> None:
        print("Пароль сброшен")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    yield UserManager(user_db)
