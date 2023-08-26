from abc import abstractmethod, ABC

from ..balance.repository import BalanceRepository
from ..category.repository import CategoryRepository
from ..transaction.repository import TransactionRepository


class IUnitOfWork(ABC):
    balance: BalanceRepository
    category: CategoryRepository
    transaction: TransactionRepository

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
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

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
