from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.schemas.post import Post, PostBase, PostCreate, PostUpdate

from ...service import post_service, user_service
from ..depends import get_db

router = APIRouter()


@router.get("/", response_model=List[Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = post_service.get_all_posts(db=db)
    return posts


@router.post("/")
def create_post(
    post: PostCreate, db: Session = Depends(get_db), authorize: AuthJWT = Depends()
):
    try:
        authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    user = user_service.get_user_by_auth(db=db, authorize=authorize)

    post_create = PostBase(
        title=post.title, text=post.text, date=post.date, user_id=user.id
    )

    post = post_service.create_post(post=post_create, db=db)
    return post


@router.delete("/{post_id}")
def delete_post(
    post_id: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()
):
    try:
        authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    user = user_service.get_user_by_auth(db=db, authorize=authorize)
    return post_service.delete_post(db=db, post_id=post_id, user_id=user.id)


@router.put("/")
def update_post(
    post: PostUpdate, db: Session = Depends(get_db), authorize: AuthJWT = Depends()
):
    try:
        authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    user = user_service.get_user_by_auth(db=db, authorize=authorize)
    post.user_id = user.id
    return post_service.update_post(db=db, post=post)
