from ..transaction.models import Transaction
from ..repositories.base_repository import SQLAlchemyRepository


class TransactionRepository(SQLAlchemyRepository):
    model = Transaction
