from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    description: str
    user_id: int
    category_id: int


    class Config:
        orm_mode = True

class ExpenseGet(ExpenseCreate):
    pass
