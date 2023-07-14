from datetime import datetime

from pydantic import BaseModel




class CategoryCreate(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class CategoryGet(CategoryCreate):
    id: int


