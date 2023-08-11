from datetime import datetime

from sqlalchemy import Integer, ForeignKey, text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import relationship

from ..balance.shemas import BalanceGet
from app.db.database import Base


class Balance(Base):
    __tablename__ = 'balance'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    total_balance: Mapped[float] = mapped_column(nullable=False, default=0)

    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship('User', back_populates='balance', uselist=False)

    transaction = relationship("Transaction", back_populates="balance")

    def to_read_model(self) -> BalanceGet:
        return BalanceGet(
            id=self.id,
            total_balance=self.total_balance,
            users_id=self.users_id
        )
