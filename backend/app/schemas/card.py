from pydantic import BaseModel
from typing import Optional
from datetime import date


class CardResponse(BaseModel):
    id: int
    title: str
    message: str
    category: Optional[str]

    class Config:
        from_attributes = True


class DailyCardResponse(BaseModel):
    card: Optional[CardResponse] = None
    assigned_at: date