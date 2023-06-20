from sqlalchemy import Column, Integer, String, DateTime, func, Float, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Income(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='incomes')