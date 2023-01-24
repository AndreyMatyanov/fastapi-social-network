from pydantic import UUID4, BaseModel, Field, validator


class UserBase(BaseModel):
    id: int
    nickname: str
    email: str
    hashed_password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    nickname: str
    email: str
    password: str


class UserUpdate(UserBase):
    pass
