from typing import Annotated, Type

from fastapi import Depends
from app.api.utils.unitofwork import UnitOfWork, IUnitOfWork
from app.db.database import async_session_maker


async def get_session() -> UnitOfWork:
    """Получение экземпляра класса сессии"""
    return UnitOfWork(session_factory=async_session_maker)


UOWDep: Type[UnitOfWork] = Annotated[UnitOfWork, Depends(get_session)]

