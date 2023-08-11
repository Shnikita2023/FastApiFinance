from datetime import datetime

from sqlalchemy import Integer, ForeignKey, String, TIMESTAMP, text, Float

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from ..transaction.shemas import TransactionGet
from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    comment: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column(nullable=False)
    type_transaction: Mapped[str] = mapped_column(String(10), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    balance_id: Mapped[int] = mapped_column(ForeignKey('balance.id'))

    user = relationship("User", back_populates="transaction")
    category = relationship("Category", back_populates="transaction")
    balance = relationship("Balance", back_populates="transaction")

    def to_read_model(self) -> TransactionGet:
        return TransactionGet(
            id=self.id,
            comment=self.comment,
            amount=self.amount,
            type_transaction=self.type_transaction,
            user_id=self.user_id,
            category_id=self.category_id,
            balance_id=self.balance_id,
            date=self.date,
        )
