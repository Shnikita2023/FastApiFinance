from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP


class BalanceCreate(BaseModel):
    total_balance: float
    user_id: int

    class Config:
        orm_mode = True


class BalanceGet(BalanceCreate):
    id: int

