from sqlalchemy import Column, Integer, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class MoodRating(Base):
    __tablename__ = "mood_ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    note = Column(Text)
    rated_at = Column(Date, default=func.current_date())
    created_at = Column(DateTime, default=func.now())