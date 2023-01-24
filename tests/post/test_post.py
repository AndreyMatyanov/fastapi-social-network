import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.schemas.post import PostBase, PostCreate, PostUpdate
from app.schemas.user import UserCreate
from app.service import auth_service, post_service

client = TestClient(app)


def test_get_posts(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    user = auth_service.create_user(db=db, user=create_user)
    post_create = PostBase(
        title="Test Title",
        text="Test Text",
        date="2023-01-22T11:30:37.260000",
        user_id=user.id,
    )
    post_service.create_post(post=post_create, db=db)

    posts = post_service.get_all_posts(db=db)

    assert posts is not None
    assert len(posts) == 1
    assert posts[0].title == post_create.title
    assert posts[0].text == post_create.text
    assert posts[0].user_id == post_create.user_id
    assert posts[0].date == post_create.date


def test_create_post(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    user = auth_service.create_user(db=db, user=create_user)
    post_create = PostBase(
        title="Test Title",
        text="Test Text",
        date="2023-01-22T11:30:37.260000",
        user_id=user.id,
    )
    post = post_service.create_post(post=post_create, db=db)
    assert post is not None
    assert post.title == post_create.title
    assert post.text == post_create.text
    assert post.user_id == post_create.user_id
    assert post.date == post_create.date


def test_update_post(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    user = auth_service.create_user(db=db, user=create_user)
    post_create = PostBase(
        title="Test Title",
        text="Test Text",
        date="2023-01-22T11:30:37.260000",
        user_id=user.id,
    )
    post = post_service.create_post(post=post_create, db=db)

    post_update = PostUpdate(
        id=post.id,
        title="Update Title",
        text="Update Text",
        date="2023-01-22T11:30:37.260000",
        user_id=user.id,
    )

    updated_post = post_service.update_post(db=db, post=post_update)
    assert updated_post is not None
    assert updated_post.id == post_update.id
    assert updated_post.title == "Update Title"
    assert updated_post.text == "Update Text"
    assert updated_post.user_id == post_update.id
    assert updated_post.date == datetime.datetime(2023, 1, 22, 11, 30, 37, 260000)


def test_delete_post(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    user = auth_service.create_user(db=db, user=create_user)
    post_create = PostBase(
        title="Test Title",
        text="Test Text",
        date="2023-01-22T11:30:37.260000",
        user_id=user.id,
    )
    post = post_service.create_post(post=post_create, db=db)

    post_deleted = post_service.delete_post(db=db, post_id=post.id, user_id=user.id)

    assert post_deleted is not None
    assert post_deleted.id == post.id
    assert post_deleted.title == post.title
    assert post_deleted.text == post.text
    assert post_deleted.user_id == post.user_id
    assert post_deleted.date == datetime.datetime(2023, 1, 22, 11, 30, 37, 260000)
