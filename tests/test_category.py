from httpx import AsyncClient, Response


class TestCategory:
    """Тест категорий"""

    async def test_add_category(self, async_client: AsyncClient, get_user_token: dict[str, str]) -> None:
        """Добавление категорий"""
        response_category: Response = await async_client.post(url="/category/",
                                                              json={"name": "Такси", "description": "такси"},
                                                              headers=get_user_token)
        assert response_category.status_code == 200, f"Ошибка добавление категории: {response_category.text}"
        assert response_category.json()["status"] == "successes"

    async def test_get_category(self, async_client: AsyncClient, get_user_token: dict[str, str]) -> None:
        """Получение категорий"""
        response_category: Response = await async_client.get(url="/category/?value=Такси&param_column=name",
                                                             headers=get_user_token)
        assert response_category.status_code == 200, f"Ошибка получение категории: {response_category.text}"
        assert response_category.json()["name"] == "Такси"
        assert response_category.json()["id"] == 1
