from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean

from app.api.expenses.models import Expense
from app.api.incomes.models import Income
from app.db.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    expenses = relationship('Expense', back_populates='user')
    incomes = relationship('Income', back_populates='user')