from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.api.depends import get_db
from app.schemas.user import UserCreate
from app.service import auth_service

router = APIRouter()


@router.post("/sing-up")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db=db, user=user)


@router.post("/login", status_code=200)
def auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    authorize: AuthJWT = Depends(),
):
    response = auth_service.login(db=db, form_data=form_data, authorize=authorize)
    return response
