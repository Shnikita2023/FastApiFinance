from typing import Any

from ..transaction.shemas import TransactionCreate, TransactionGet
from ..utils.unitofwork import IUnitOfWork


class TransactionService:
    async def add_transaction(self, new_transaction: TransactionCreate, uow: IUnitOfWork) -> int:
        balance_id = new_transaction.balance_id
        category_amount = new_transaction.amount
        async with uow:
            now_balance = await uow.balance.find_one(balance_id)
            if new_transaction.type_transaction == "Доход":
                new_balance = now_balance.total_balance + category_amount
            else:
                new_balance = now_balance.total_balance - category_amount
            transaction_id = await uow.transaction.add_one(new_transaction.dict())
            new_balance = {"total_balance": new_balance}
            await uow.balance.update_one(balance_id, new_balance)
            await uow.commit()
            return transaction_id

    async def get_transactions(self, uow: IUnitOfWork) -> list[TransactionGet]:
        async with uow:
            all_transaction = await uow.transaction.find_all()
            return all_transaction

    async def get_transaction(self, transaction_id: int, uow: IUnitOfWork) -> TransactionGet:
        async with uow:
            one_transaction = await uow.transaction.find_one(transaction_id)
            return one_transaction

    async def get_transaction_by_param(self,
                                       value: Any,
                                       uow: IUnitOfWork,
                                       param_column: str = "user_id") -> list[TransactionGet]:
        async with uow:
            all_transaction = await uow.transaction.find_by_param(param_column, value)
            return all_transaction

    async def get_transaction_by_param_limit(self,
                                             value: Any,
                                             page: int,
                                             size: int,
                                             uow: IUnitOfWork,
                                             param_column: str = "user_id") -> list[TransactionGet]:
        async with uow:
            limit_transaction = await uow.transaction.find_by_param_limit(param_column, value, page, size)
            return limit_transaction

    async def delete_transaction(self, transaction_id: int, uow: IUnitOfWork) -> int:
        async with uow:
            one_transaction = await uow.transaction.delete_one(transaction_id)
            await uow.commit()
            return one_transaction
