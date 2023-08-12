from typing import Any

from ..balance.shemas import BalanceGet
from ..utils.unitofwork import IUnitOfWork


class BalanceService:
    async def add_balance(self, user_id: int, uow: IUnitOfWork) -> int:
        balance_dict = {"users_id": user_id}
        async with uow:
            balance_id = await uow.balance.add_one(data=balance_dict)
            await uow.commit()
            return balance_id

    async def get_balance(self, balance_id: int, uow) -> BalanceGet:
        async with uow:
            one_balance = await uow.balance.find_one(balance_id)
            return one_balance

    async def get_balance_by_param(self,
                                   value: Any,
                                   uow: IUnitOfWork,
                                   param_column: str = "users_id") -> BalanceGet:
        async with uow:
            one_balance = await uow.balance.find_by_param(param_column, value)
            return one_balance[0] if len(one_balance) > 0 else one_balance

    async def update_balance(self,
                             balance_id: int,
                             new_data: float,
                             uow: IUnitOfWork) -> dict:
        new_data = {"total_balance": new_data}
        async with uow:
            new_balance = await uow.balance.update_one(balance_id, new_data)
            await uow.commit()
            return new_balance

    async def delete_balance(self,
                             balance_id: int,
                             uow: IUnitOfWork) -> int:
        async with uow:
            new_balance = await uow.balance.delete_one(balance_id)
            await uow.commit()
            return new_balance
