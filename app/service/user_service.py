from typing import List

from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.crud.user_crud import user_crud
from app.schemas.user import UserBase


def get_all_users(db: Session) -> List[UserBase]:
    user_db = user_crud.get_multi(db=db)
    return [UserBase.from_orm(user) for user in user_db]


def get_user_by_auth(db: Session, authorize: AuthJWT):
    current_user = authorize.get_jwt_subject()
    user_db = user_crud.get_user_by_email(db=db, email=current_user)
    return UserBase.from_orm(user_db)
