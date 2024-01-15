from fastapi import FastAPI

from api.users.controllers.users_controller import users
from api.classes.controllers.classes_controller import classes

from api.database import engine

from api.config import DevelopmentConfig

from api.system.models.models import Base

from api.utils.singleton import singleton


@singleton
def create_app(config_class=DevelopmentConfig):
    app = FastAPI()
    app.config = config_class

    Base.metadata.create_all(bind=engine)

    app.include_router(users, tags=["users"])
    app.include_router(classes, tags=["classes"])

    return app
