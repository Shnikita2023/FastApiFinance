from httpx import AsyncClient



async def test_add_category(async_client: AsyncClient, user_token: dict) -> None:
    """Добавление категорий"""
    response_category = await async_client.post(url="/category/add",
                                                json={"name": "Такси", "description": "такси"},
                                                headers=user_token)
    assert response_category.status_code == 200, f"Ошибка добавление категории: {response_category.text}"
    assert response_category.json()["status"] == "successes"
    assert response_category.json()["data"] == "product Такси added"


async def test_get_category(async_client: AsyncClient) -> None:
    """Получение категорий"""
    response_category = await async_client.get(url="/category/?category_name=Такси")
    assert response_category.status_code == 200, f"Ошибка получение категории: {response_category.text}"
    assert response_category.json()["name"] == "Такси"
    assert response_category.json()["id"] == 1



