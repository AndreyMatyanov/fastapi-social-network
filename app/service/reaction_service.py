from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.post_crud import post_crud
from app.crud.reaction_crud import reaction_crud
from app.schemas.post import Post
from app.schemas.reaction import Reaction, ReactionBase


def set_reaction(db: Session, reaction: ReactionBase):
    reaction_db = reaction_crud.get_by_user_id_and_post_id(db=db, reaction=reaction)
    if reaction_db:
        raise HTTPException(status_code=400, detail="Reaction is already set.")

    post_db = post_crud.get(db=db, id=reaction.post_id)
    post = Post.from_orm(post_db)
    if post.user_id == reaction.user_id:
        raise HTTPException(
            status_code=400, detail="You can't set reaction on your posts."
        )

    reaction_db = reaction_crud.create(db=db, obj_in=reaction)
    return Reaction.from_orm(reaction_db)


def get_count_of_reactions(post_id: int, db: Session):
    counts = reaction_crud.get_counts_on_post(db=db, post_id=post_id)
    return counts
