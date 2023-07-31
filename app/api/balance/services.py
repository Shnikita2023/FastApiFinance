from typing import Any

from ..balance.shemas import BalanceGet
from ..repositories.base_repository import AbstractRepository

from ..services.base_service import BaseService


class BalanceService(BaseService):
    def __init__(self, balance_repo: AbstractRepository):
        self.balance_repo: AbstractRepository
        super().__init__(balance_repo)

    async def add_balance(self, user_id: int) -> int:
        balance_dict = {"users_id": user_id}
        balance_id = await self.add_one(balance_dict)
        return balance_id

    async def get_balance(self, balance_id: int) -> BalanceGet:
        one_balance = await self.find_one(balance_id)
        return one_balance

    async def get_balance_by_param(self, value: Any, param_column: str = "users_id") -> BalanceGet:
        one_balance = await self.find_by_param(param_column, value)
        return one_balance[0]

    async def update_balance(self, balance_id: int, new_data: float) -> dict:
        new_data = {"total_balance": new_data}
        new_balance = await self.update_one(balance_id, new_data)
        return new_balance
