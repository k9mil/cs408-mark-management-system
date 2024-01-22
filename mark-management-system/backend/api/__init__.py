import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.users.controllers.users_controller import users
from api.classes.controllers.classes_controller import classes
from api.roles.controllers.roles_controller import roles
from api.students.controllers.students_controller import students

from api.database import engine

from api.config import DevelopmentConfig

from api.system.models.models import Base

from api.utils.singleton import singleton


@singleton
def create_app(config_class=DevelopmentConfig):
    app = FastAPI()
    app.config = config_class

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(users, tags=["users"])
    app.include_router(classes, tags=["classes"])
    app.include_router(roles, tags=["roles"])
    app.include_router(students, tags=["students"])

    return app
