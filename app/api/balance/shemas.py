from pydantic import BaseModel


class BalanceCreate(BaseModel):
    amount: float
    user_id: int


    class Config:
        orm_mode = True

class BalanceGet(BalanceCreate):
    pass
