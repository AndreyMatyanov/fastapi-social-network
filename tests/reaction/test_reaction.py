from datetime import datetime

from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.schemas.post import PostBase
from app.schemas.reaction import ReactionBase
from app.schemas.user import UserCreate
from app.service import auth_service, post_service, reaction_service

client = TestClient(app)


def test_set_reaction(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    user_author = auth_service.create_user(db=db, user=create_user)

    post_create = PostBase(
        title="Test Title",
        text="Test Text",
        date="2023-01-22T11:30:37.260000",
        user_id=user_author.id,
    )
    post = post_service.create_post(post=post_create, db=db)

    create_user = UserCreate(
        nickname="SecondUser", email="test2@gmail.com", password="test"
    )
    user_viewer = auth_service.create_user(db=db, user=create_user)

    reaction_create = ReactionBase(
        post_id=post.id,
        user_id=user_viewer.id,
        reaction="LIKE",
        date="2023-01-22T11:30:37.260000",
    )

    reaction = reaction_service.set_reaction(db=db, reaction=reaction_create)

    assert reaction is not None
    assert reaction.post_id == post.id
    assert reaction.user_id == user_viewer.id
    assert reaction.date == datetime(2023, 1, 22, 11, 30, 37, 260000)
    assert reaction.reaction == reaction_create.reaction


def test_get_count_of_reactions(db: Session):
    create_user = UserCreate(nickname="test", email="test@gmail.com", password="test")
    user_author = auth_service.create_user(db=db, user=create_user)

    post_create = PostBase(
        title="Test Title",
        text="Test Text",
        date="2023-01-22T11:30:37.260000",
        user_id=user_author.id,
    )
    post = post_service.create_post(post=post_create, db=db)

    create_user = UserCreate(
        nickname="SecondUser", email="test2@gmail.com", password="test"
    )
    user_viewer = auth_service.create_user(db=db, user=create_user)

    reaction_create = ReactionBase(
        post_id=post.id,
        user_id=user_viewer.id,
        reaction="LIKE",
        date="2023-01-22T11:30:37.260000",
    )

    reaction_service.set_reaction(db=db, reaction=reaction_create)

    reactions_post = reaction_service.get_count_of_reactions(post_id=post.id, db=db)

    assert reactions_post is not None
    assert reactions_post.like == 1
    assert reactions_post.dislike == 0


def test_set_like_on_own_post(db: Session):
    try:
        create_user = UserCreate(
            nickname="test", email="test@gmail.com", password="test"
        )
        user_author = auth_service.create_user(db=db, user=create_user)

        post_create = PostBase(
            title="Test Title",
            text="Test Text",
            date="2023-01-22T11:30:37.260000",
            user_id=user_author.id,
        )
        post = post_service.create_post(post=post_create, db=db)

        reaction_create = ReactionBase(
            post_id=post.id,
            user_id=user_author.id,
            reaction="LIKE",
            date="2023-01-22T11:30:37.260000",
        )

        reaction_service.set_reaction(db=db, reaction=reaction_create)
        assert False
    except HTTPException:
        assert True
