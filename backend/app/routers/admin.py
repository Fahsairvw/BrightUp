from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.card import Card
from app.models.mood import MoodRating
from app.models.user import User
from app.schemas.card import CardResponse
from app.routers.mood import get_current_user_id
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


# Schemas for card create/edit
class CardRequest(BaseModel):
    title: str
    message: str
    category: Optional[str] = None


# Check if current user role is admin
def require_admin(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user_id


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    user_id: int = Depends(require_admin)
):
    total_users = db.query(User).filter(User.role == "user").count()
    total_ratings = db.query(MoodRating).count()
    total_cards = db.query(Card).filter(Card.is_active == True).count()
    avg_rating = db.query(MoodRating).all()
    avg = round(sum(m.rating for m in avg_rating) / len(avg_rating), 2) if avg_rating else 0

    return {
        "total_users": total_users,
        "total_ratings": total_ratings,
        "total_active_cards": total_cards,
        "average_mood_rating": avg
    }


@router.post("/cards", response_model=CardResponse)
def create_card(
    req: CardRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_admin)
):
    card = Card(title=req.title, message=req.message, category=req.category, created_by=user_id)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.put("/cards/{card_id}", response_model=CardResponse)
def edit_card(
    card_id: int,
    req: CardRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_admin)
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card.title = req.title
    card.message = req.message
    card.category = req.category
    db.commit()
    db.refresh(card)
    return card


@router.delete("/cards/{card_id}")
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_admin)
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card.is_active = False   # soft delete
    db.commit()
    return {"message": "Card deleted successfully"}
