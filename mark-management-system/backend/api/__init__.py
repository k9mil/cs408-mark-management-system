from fastapi import FastAPI

from api.marks.controllers.mark_controller import marks

from api.config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = FastAPI()
    app.config = config_class

    app.include_router(marks)

    return app