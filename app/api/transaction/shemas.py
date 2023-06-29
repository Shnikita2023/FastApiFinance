from pydantic import BaseModel
from enum import Enum


class TypeTranstaction(Enum):
    INCOME = "Доход"
    EXPENSE = "Расход"


class TransactionCreate(BaseModel):
    comment: str | None = None
    amount: float
    type_transaction: TypeTranstaction
    user_id: int
    category_id: int


    class Config:
        orm_mode = True

class TransactionGet(TransactionCreate):
    pass
