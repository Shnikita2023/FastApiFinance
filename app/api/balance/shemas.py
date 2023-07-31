from pydantic import BaseModel


class BalanceCreate(BaseModel):
    total_balance: float
    users_id: int

    class Config:
        orm_mode = True


class BalanceGet(BalanceCreate):
    id: int


class BalanceUpdate(BaseModel):
    total_balance: float

