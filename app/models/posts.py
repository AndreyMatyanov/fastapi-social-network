from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db import Base
from app.models.users import User


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String)
    text = Column(String(length=2000))
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
