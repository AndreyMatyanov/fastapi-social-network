from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.post_crud import post_crud
from app.models import Post
from app.schemas.post import Post as PostSchema
from app.schemas.post import PostBase, PostCreate, PostUpdate


def get_all_posts(db: Session):
    posts_db: List[Post] = post_crud.get_multi(db=db)
    return [PostSchema.from_orm(mission) for mission in posts_db]


def get_by_id(db: Session, post_id: int):
    post_db: Post = post_crud.get(db=db, id=post_id)
    return PostSchema.from_orm(post_db)


def create_post(db: Session, post: PostBase):
    post_db = post_crud.create(db=db, obj_in=post)
    return PostSchema.from_orm(post_db)


def delete_post(db: Session, post_id: int, user_id: int):
    post = get_by_id(db=db, post_id=post_id)
    if post.user_id is not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="It's not your post."
        )
    post_db = post_crud.remove(db=db, id=post_id)
    return PostSchema.from_orm(post_db)


def update_post(post: PostUpdate, db: Session):
    post_db = post_crud.get(db=db, id=post.id)
    post_upd = post_crud.update(db=db, db_obj=post_db, obj_in=post)
    return PostSchema.from_orm(post_upd)
