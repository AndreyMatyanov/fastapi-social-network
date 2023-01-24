from fastapi.security import OAuth2PasswordBearer

from ..db.database import SessionLocal

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
