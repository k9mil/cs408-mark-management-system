from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from api.config import DevelopmentConfig
from api.config import TestingConfig


database_url = DevelopmentConfig.DATABASE_URL or TestingConfig.DATABASE_URL

if database_url:
    engine = create_engine(database_url)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """A generator that provides a session database pool."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
