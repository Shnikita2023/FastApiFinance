from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..users.models import User
from app.db.database import get_async_session
from ..users.services import CustomUserDatabase


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> CustomUserDatabase:
    yield CustomUserDatabase(session, User)
