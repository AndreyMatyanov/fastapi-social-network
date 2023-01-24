import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    authjwt_secret_key: str = (
        "b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405"
    )

    class Config:
        env_file = ".env"


settings = Settings(_env_file=os.getenv("APP_CONFIG"), _env_file_encoding="utf-8")
