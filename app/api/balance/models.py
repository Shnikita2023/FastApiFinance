from sqlalchemy import Column, Integer, ForeignKey, Float, text, TIMESTAMP

from sqlalchemy.orm import relationship

from app.db.database import Base


class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    income = Column(Float, nullable=False, default=0)
    expense = Column(Float, nullable=False, default=0)
    total_balance = Column(Float, nullable=False)

    users_id = Column(Integer, ForeignKey("users_id"))
    user = relationship('User', back_populates='balance', uselist=False)

    transactions = relationship("Transaction", back_populates="balance")

