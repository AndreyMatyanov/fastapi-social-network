from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.main import app
from app.schemas.user import UserCreate
from app.service import auth_service

client = TestClient(app)
authorize = AuthJWT()


def test_create_user(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    user = auth_service.create_user(db=db, user=create_user)
    assert user.nickname == create_user.nickname


def test_login(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    auth_service.create_user(db=db, user=create_user)
    form_data = OAuth2PasswordRequestForm(
        username="test@gmail.com", password="test", scope=""
    )
    response = auth_service.login(db=db, form_data=form_data, authorize=authorize)
    assert response is not None
    assert response.access is not None
    assert response.refresh is not None
