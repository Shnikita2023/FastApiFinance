from typing import Any

from ..repositories.base_repository import AbstractRepository


class BaseService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def add_one(self, data: Any) -> int:
        item_id = await self.repository.add_one(data)
        return item_id

    async def find_one(self, item_id: int) -> Any:
        item = await self.repository.find_one(item_id)
        return item

    async def find_all(self) -> list:
        items = await self.repository.find_all()
        return items

    async def find_by_param(self, param_column: str, value: Any) -> Any:
        items = await self.repository.find_by_param(param_column, value)
        return items

    async def find_by_param_limit(self, param_column: str, value: Any, index: int, count: int) -> Any:
        items = await self.repository.find_by_param_limit(param_column, value, index, count)
        return items

    async def update_one(self, item_id: int, new_data: Any) -> Any:
        updated_item = await self.repository.update_one(item_id, new_data)
        return updated_item

    async def delete_one(self, item_id: int) -> int:
        deleted_item_id = await self.repository.delete_one(item_id)
        return deleted_item_id
