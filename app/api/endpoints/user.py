from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.depends import get_db
from app.service import user_service

router = APIRouter()


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db=db)
