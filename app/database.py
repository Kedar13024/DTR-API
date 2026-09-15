"""SQLAlchemy database engine, session, and base-model configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker , Session
from app.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False , bind=engine)

class Base(DeclarativeBase):
    """Provide the declarative base class for all ORM models."""

    pass

def get_db():
    """Provide one database session per request and close it afterwards.

    Yields:
        Session: An active SQLAlchemy database session.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

