from typing import Optional

from sqlalchemy.orm import Session, with_polymorphic

from app.crud.base import CRUDBase
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).one_or_none()


user_crud = CRUDUser(User)
