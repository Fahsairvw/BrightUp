from pydantic import BaseModel
from typing import Optional
from datetime import date


class MoodRequest(BaseModel):
    rating: int        # 1-5
    note: Optional[str] = None


class MoodResponse(BaseModel):
    id: int
    rating: int
    note: Optional[str]
    rated_at: date

    class Config:
        from_attributes = True
