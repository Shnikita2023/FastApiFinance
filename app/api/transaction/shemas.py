from typing import Literal

from pydantic import BaseModel
from enum import Enum




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
    pass
