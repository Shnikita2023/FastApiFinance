from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category_id: int

    class Config:
        orm_mode = True

class Expense(ExpenseCreate):
    pass
