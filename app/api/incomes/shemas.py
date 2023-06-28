from pydantic import BaseModel


class IncomeCreate(BaseModel):
    amount: float
    description: str
    user_id: int
    category_id: int

    class Config:
        orm_mode = True

class IncomeGet(IncomeCreate):
    pass
