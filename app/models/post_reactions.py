from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db import Base
from app.models.users import User


class PostReactions(Base):
    __tablename__ = "post_reactions"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    reaction = Column(String)
    date = Column(DateTime, nullable=False)
