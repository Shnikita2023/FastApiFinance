from sqlalchemy import Column, Integer, String, DateTime, func

from sqlalchemy.orm import relationship

from app.db.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # expenses = relationship('Expense', back_populates='category')
    # incomes = relationship('Income', back_populates='category')
    transaction = relationship('Transaction', back_populates='category')
