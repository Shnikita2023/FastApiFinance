from httpx import AsyncClient, Response


class TestBalance:
    """Тест баланса"""

    async def test_get_balance_by_param(self, async_client: AsyncClient, get_user_token: dict[str, str]) -> None:
        """Функция на получение баланса"""
        response_balance: Response = await async_client.get(url="/balance/", headers=get_user_token)
        assert response_balance.status_code == 200, f"Ошибка получение пользователя: {response_balance.text}"
        assert response_balance.json()["total_balance"] == 0
        assert response_balance.json()["id"] == 1
