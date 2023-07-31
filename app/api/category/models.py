from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from ..category.shemas import CategoryGet
from app.db.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    transaction = relationship('Transaction', back_populates='category')

    def to_read_model(self) -> CategoryGet:
        return CategoryGet(
            id=self.id,
            name=self.name,
            description=self.description,
        )
