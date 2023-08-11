from abc import abstractmethod, ABC
from typing import Type

from ..balance.repository import BalanceRepository
from ..category.repository import CategoryRepository
from ..transaction.repository import TransactionRepository
from ...db.database import async_session_maker


class IUnitOfWork(ABC):
    balance: Type[BalanceRepository]
    category: Type[CategoryRepository]
    transaction: Type[TransactionRepository]

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    async def __aenter__(self) -> None:
        ...

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

        self.balance = BalanceRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.transaction = TransactionRepository(self.session)

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

