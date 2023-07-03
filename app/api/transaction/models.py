from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, text, Float

from sqlalchemy.orm import relationship

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    comment = Column(String)
    amount = Column(Float, nullable=False)
    type_transaction = Column(String(10), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    balance_id = Column(Integer, ForeignKey('balance.id'))

    user = relationship("User", back_populates="transaction")
    category = relationship("Category", back_populates="transaction")
    balance = relationship("Balance", back_populates="transaction")
