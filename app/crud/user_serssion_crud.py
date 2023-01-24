from app.crud.base import CRUDBase
from app.models.tokens import UserSession


class CRUDSession(CRUDBase[UserSession, CreateUserSession, UpdateUserSession]):
    pass


user_session_crud = CRUDSession(UserSession)
