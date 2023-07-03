from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str = Field(max_length=50)
    username: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    registered_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str 
    last_name: str
    first_name: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False