from ..balance.repository import BalanceRepository
from ..category.repository import CategoryRepository
from ..transaction.repository import TransactionRepository
from ..balance.services import BalanceService
from ..category.services import CategoryService
from ..transaction.services import TransactionService


def category_service():
    return CategoryService(CategoryRepository())


def balance_service():
    return BalanceService(BalanceRepository())


def transaction_service():
    return TransactionService(TransactionRepository())
