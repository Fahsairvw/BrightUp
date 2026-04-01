from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())


class UserDailyCard(Base):
    __tablename__ = "user_daily_cards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    assigned_at = Column(Date, default=func.current_date())
