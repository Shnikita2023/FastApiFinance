from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    comment: str | None = None
    amount: float
    type_transaction: Literal["Доход", "Расход"]
    user_id: int
    category_id: int
    balance_id: int

    class Config:
        orm_mode = True


class TransactionGet(TransactionCreate):
    id: int
    date: datetime
