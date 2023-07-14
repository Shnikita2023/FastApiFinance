from tests.conftest import client


class TestPositiveAuth:

    async def test_register_user(self) -> None:
        """Регистрация пользователя"""
        response = client.post(url="/auth/register", json={
            "email": "nikita@mail.ru",
            "password": "string1",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string1",
            "last_name": "string1",
            "first_name": "string1"
        })
        assert response.status_code == 201, "Ошибка в регистрации пользователя"
        assert len(response.json()) == 9
        assert response.json()["id"] == 1
        assert response.json()["username"] == "string1"
        assert response.json()["email"] == "nikita@mail.ru"

    async def test_auth_user(self) -> None:
        """Авторизация пользователя"""
        response_auth = client.post(url="/auth/jwt/login", data={
            "username": "nikita@mail.ru",
            "password": "string1",
        })
        assert response_auth.status_code == 204, "Ошибка авторизации"

    async def test_get_user(self, user_token: dict) -> None:
        """Получение данных пользователя"""
        response_authentic = client.get(url="/authentic/me", headers=user_token)
        assert response_authentic.status_code == 200, "Данные о пользователе не получены"
        assert response_authentic.json()["id"] == 2
        assert response_authentic.json()["username"] == "Nikita"
        assert response_authentic.json()["email"] == "usertest@mail.ru"
