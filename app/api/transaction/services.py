from typing import Any

from ..balance.services import BalanceService
from ..repositories.base_repository import AbstractRepository
from ..services.base_service import BaseService
from ..transaction.shemas import TransactionCreate, TransactionGet



class TransactionService(BaseService):
    def __init__(self, transaction_repo: AbstractRepository):
        self.transaction_repo: AbstractRepository
        super().__init__(transaction_repo)

    async def add_transaction(self, new_transaction: TransactionCreate, balance_service: BalanceService) -> int:
        balance_id = new_transaction.balance_id
        category_amount = new_transaction.amount
        now_balance = await balance_service.get_balance(balance_id)
        if new_transaction.type_transaction == "Доход":
            new_balance = now_balance.total_balance + category_amount
        else:
            new_balance = now_balance.total_balance - category_amount
        transaction_id = await self.add_one(new_transaction.dict())
        try:
            await balance_service.update_balance(balance_id, new_balance)

        except Exception as ex:
            await self.delete_one(transaction_id)  # Откатываем транзакцию, удаление объекта
            raise ex

        return transaction_id

    async def get_transactions(self) -> list[TransactionGet]:
        all_transaction = await self.find_all()
        return all_transaction

    async def get_transaction(self, id_category: int) -> TransactionGet:
        one_transaction = await self.find_one(id_category)
        return one_transaction

    async def get_transaction_by_param(self, value: Any, param_column: str = "user_id") -> list[TransactionGet]:
        all_transaction = await self.find_by_param(param_column, value)
        return all_transaction

    async def get_transaction_by_param_limit(self,
                                             value: Any,
                                             page: int,
                                             size: int,
                                             param_column: str = "user_id") -> list[TransactionGet]:

        limit_transaction = await self.find_by_param_limit(param_column, value, page, size)
        return limit_transaction

    async def delete_transaction(self, transaction_id: int) -> int:
        one_transaction = await self.delete_one(transaction_id)
        return one_transaction
