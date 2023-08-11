from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class CategoryGet(CategoryCreate):
    id: int
