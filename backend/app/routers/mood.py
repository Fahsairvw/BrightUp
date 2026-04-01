from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.models.mood import MoodRating
from app.schemas.mood import MoodRequest, MoodResponse
from app.config import settings

router = APIRouter(prefix="/mood", tags=["Mood"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/rate", response_model=MoodResponse)
def rate_mood(
    req: MoodRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Validate rating 1-5
    if req.rating < 1 or req.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    # Check if already rated today
    today = date.today()
    existing = db.query(MoodRating).filter(
        MoodRating.user_id == user_id,
        MoodRating.rated_at == today
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already rated today!")

    mood = MoodRating(user_id=user_id, rating=req.rating, note=req.note)
    db.add(mood)
    db.commit()
    db.refresh(mood)
    return mood


@router.get("/history", response_model=list[MoodResponse])
def get_history(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    moods = db.query(MoodRating).filter(
        MoodRating.user_id == user_id
    ).order_by(MoodRating.rated_at.desc()).all()
    return moods
