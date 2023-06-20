from pydantic import BaseModel


class IncomeCreate(BaseModel):
    amount: float
    description: str

    class Config:
        orm_mode = True

class Income(IncomeCreate):
    pass
