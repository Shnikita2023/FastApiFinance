from typing import Any

from ..category.shemas import CategoryCreate, CategoryGet
from ..repositories.base_repository import AbstractRepository
from ..services.base_service import BaseService


class CategoryService(BaseService):
    def __init__(self, category_repo: AbstractRepository):
        self.category_repo: AbstractRepository
        super().__init__(category_repo)

    async def add_category(self, category: CategoryCreate) -> int:
        category_dict = category.dict()
        category_id = await self.add_one(category_dict)
        return category_id

    async def get_categories(self) -> list[CategoryGet]:
        all_category = await self.find_all()
        return all_category

    async def get_category(self, id_category: int) -> CategoryGet:
        one_category = await self.find_one(id_category)
        return one_category

    async def get_category_by_param(self, param_column: str, value: Any) -> CategoryGet:
        one_category = await self.find_by_param(param_column, value)
        return one_category[0]

    async def delete_category(self, category_id: int) -> int:
        id_category = await self.delete_one(category_id)
        return id_category
