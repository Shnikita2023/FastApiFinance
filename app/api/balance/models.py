from sqlalchemy import Column, Integer, ForeignKey, Float, text, TIMESTAMP

from sqlalchemy.orm import relationship

from app.db.database import Base


class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    total_balance = Column(Float, nullable=False, default=0)

    users_id = Column(Integer, ForeignKey("users.id"))
    user = relationship('User', back_populates='balance', uselist=False)

    transaction = relationship("Transaction", back_populates="balance")

