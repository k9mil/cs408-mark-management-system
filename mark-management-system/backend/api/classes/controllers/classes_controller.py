from fastapi import Depends, APIRouter, HTTPException

from api.system.schemas import schemas

from api.users.repositories.user_repository import UserRepository

from api.classes.use_cases.create_class_use_case import CreateClassUseCase

from api.classes.errors.class_already_exists import ClassAlreadyExists
from api.users.errors.user_not_found import UserNotFound

from api.classes.dependencies import create_class_use_case


classes = APIRouter()


@classes.post("/classes/", response_model=schemas.Class)
def create_class(
    request: schemas.ClassCreate,
    create_class_use_case: CreateClassUseCase = Depends(create_class_use_case),
):
    try:
        return create_class_use_case.execute(
            request,
        )
    except ClassAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))