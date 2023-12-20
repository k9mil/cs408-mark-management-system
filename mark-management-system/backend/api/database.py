from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from api.config import DevelopmentConfig


database_url = DevelopmentConfig.DATABASE_URL
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
