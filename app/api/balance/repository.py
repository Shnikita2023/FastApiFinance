from ..balance.models import Balance
from ..repositories.base_repository import SQLAlchemyRepository


class BalanceRepository(SQLAlchemyRepository):
    model = Balance
