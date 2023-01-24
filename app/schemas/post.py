from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str
    date: datetime
    user_id: int


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    text: str
    date: datetime


class PostUpdate(Post):
    pass
