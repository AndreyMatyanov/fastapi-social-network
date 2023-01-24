from sqlalchemy import Column, Integer, String

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    nickname = Column(String, nullable=False)
    email = Column(String(40), unique=True, index=True)
    hashed_password = Column(String)
