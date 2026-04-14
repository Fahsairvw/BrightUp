from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.database import get_db
from app.models.card import Card, UserDailyCard
from app.schemas.card import CardResponse, DailyCardResponse
from app.config import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/cards", tags=["Cards"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_optional_user_id(token: Optional[str] = Depends(oauth2_scheme)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        return None


@router.get("/all", response_model=list[CardResponse])
def get_all_cards(db: Session = Depends(get_db)):
    cards = db.query(Card).filter(Card.is_active == True).all()
    return cards


@router.get("/today", response_model=DailyCardResponse)
def get_today_card(
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_optional_user_id)
):
    today = date.today()

    if user_id:
        existing = db.query(UserDailyCard).filter(
            UserDailyCard.user_id == user_id,
            UserDailyCard.assigned_at == today
        ).first()
        if existing:
            card = db.query(Card).filter(Card.id == existing.card_id).first()
            return {"card": card, "assigned_at": today}

    return {"card": None, "assigned_at": today}


@router.post("/pick/{card_id}", response_model=DailyCardResponse)
def pick_card(
    card_id: int,
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_optional_user_id)
):
    today = date.today()
    card = db.query(Card).filter(Card.id == card_id, Card.is_active == True).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    if user_id:
        # Check if already picked today
        existing = db.query(UserDailyCard).filter(
            UserDailyCard.user_id == user_id,
            UserDailyCard.assigned_at == today
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="You already picked a card today!")

        assignment = UserDailyCard(user_id=user_id, card_id=card.id)
        db.add(assignment)
        db.commit()

    return {"card": card, "assigned_at": today}
