from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import EnumBaseUpper


class TypeOfReaction(EnumBaseUpper):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"


class ReactionBase(BaseModel):
    post_id: int
    user_id: int
    reaction: TypeOfReaction
    date: datetime


class ReactionCreate(BaseModel):
    post_id: int
    reaction: TypeOfReaction
    date: datetime


class Reaction(ReactionBase):
    id: int

    class Config:
        orm_mode = True


class ReactionUpdate(Reaction):
    pass


class ReactionDelete(BaseModel):
    user_id: int
    post_id: int


class CountOfReactions(BaseModel):
    like: int
    dislike: int
