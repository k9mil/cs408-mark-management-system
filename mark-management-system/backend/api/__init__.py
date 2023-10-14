from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.marks.controllers.mark_controller import marks

from api.config import DevelopmentConfig
from api.system.models.models import Base

from api.utils.singleton import singleton


database_url = DevelopmentConfig.DATABASE_URL
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@singleton
def create_app(config_class=DevelopmentConfig):
    app = FastAPI()
    app.config = config_class

    Base.metadata.create_all(bind=engine)

    app.include_router(marks)

    return app

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
