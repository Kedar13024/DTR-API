
"""Application configuration loaded from environment variables."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Define and validate settings required by the application.

    Attributes:
        database_user: PostgreSQL username.
        database_password: PostgreSQL password.
        database_host: PostgreSQL host name.
        database_port: PostgreSQL port.
        database_name: PostgreSQL database name.
        secret_key: Secret used to sign JWTs.
        algorithm: JWT signing algorithm.
        access_token_expire_minutes: JWT lifetime in minutes.
    """

    database_user : str
    database_password : str
    database_host : str
    database_port : str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env")


settings = Settings()
