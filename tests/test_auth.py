from tests.conftest import client
from requests import Response


class TestPositiveAuth:
    """Тест пользователя"""

    async def test_register_user(self) -> None:
        """Регистрация пользователя"""
        response: Response = client.post(url="/auth/register", json={
            "email": "nikita@mail.ru",
            "password": "string1fadH!",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "ivanov",
            "last_name": "Ivanov",
            "first_name": "Ivan"
        })
        assert response.status_code == 201, f"Ошибка при создании пользователя: {response.text}"
        assert len(response.json()) == 9
        assert response.json()["id"] == 1
        assert response.json()["username"] == "ivanov"
        assert response.json()["email"] == "nikita@mail.ru"

    async def test_auth_user(self) -> None:
        """Авторизация пользователя"""
        response_auth: Response = client.post(url="/auth/jwt/login", data={
            "username": "nikita@mail.ru",
            "password": "string1fadH!",
        })
        assert response_auth.status_code == 204 or 200, f"Ошибка авторизации: {response_auth.text}"

    async def test_get_data_user(self, get_user_token: dict[str, str]) -> None:
        """Получение данных пользователя"""
        response_authentic: Response = client.get(url="/users/me", headers=get_user_token)
        assert response_authentic.status_code == 200, f"Ошибка получение данных пользователя: {response_authentic.text}"
        assert response_authentic.json()["id"] == 1 or 2
        assert response_authentic.json()["username"] == "ivan"
        assert response_authentic.json()["email"] == "usertest@mail.ru"
