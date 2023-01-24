from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class SessionBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"
    user_id: int

    class Config:
        allow_population_by_field_name = (True,)
        orm_mode = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class ResponseToken(BaseModel):
    access: str
    refresh: str

    class Config:
        orm_mode = True
