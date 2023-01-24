from typing import Optional

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.config.security import get_random_string, hash_password, validate_password
from app.crud.user_crud import user_crud
from app.models import User
from app.schemas.session import ResponseToken
from app.schemas.user import UserBase, UserCreate


def create_user(user: UserCreate, db: Session):
    db_user = user_crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail="User with this email is already registered"
        )
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    user_model = User(
        nickname=user.nickname, email=user.email, hashed_password=hashed_password
    )
    user_db: User = user_crud.create(db=db, obj_in=user_model.__dict__)
    return UserBase.from_orm(user_db)


def login(form_data: OAuth2PasswordRequestForm, db: Session, authorize: AuthJWT):
    user: Optional[User] = user_crud.get_user_by_email(db=db, email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not validate_password(
        password=form_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = authorize.create_access_token(subject=user.email)
    refresh_token = authorize.create_refresh_token(subject=user.email)

    response = ResponseToken(access=access_token, refresh=refresh_token)
    return response
