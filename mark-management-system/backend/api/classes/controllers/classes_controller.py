from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple

from api.system.schemas import schemas

from api.classes.use_cases.create_class_use_case import CreateClassUseCase
from api.classes.use_cases.get_classes_use_case import GetClassesUseCase
from api.classes.use_cases.get_classes_for_lecturer_use_case import GetClassesForLecturerUseCase
from api.classes.use_cases.edit_class_use_case import EditClassUseCase
from api.classes.use_cases.delete_class_use_case import DeleteClassUseCase
from api.classes.use_cases.get_class_use_case import GetClassUseCase

from api.classes.errors.class_already_exists import ClassAlreadyExists
from api.classes.errors.classes_not_found import ClassesNotFound
from api.classes.errors.class_not_found import ClassNotFound

from api.users.errors.user_not_found import UserNotFound

from api.classes.dependencies import create_class_use_case
from api.classes.dependencies import get_classes_use_case
from api.classes.dependencies import get_classes_for_lecturer_use_case
from api.classes.dependencies import edit_class_use_case
from api.classes.dependencies import delete_class_use_case
from api.classes.dependencies import get_class_use_case

from api.middleware.dependencies import get_current_user


classes = APIRouter()


@classes.post("/classes/", response_model=schemas.Class)
def create_class(
    request: schemas.ClassCreate,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    create_class_use_case: CreateClassUseCase = Depends(create_class_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return create_class_use_case.execute(
            request, current_user
        )
    except ClassAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.get("/classes/", response_model=list[schemas.Class])
def get_classes(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_classes_use_case: GetClassesUseCase = Depends(get_classes_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_classes_use_case.execute(skip, limit, current_user)
    except ClassesNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@classes.get("/classes/lecturer", response_model=list[schemas.Class])
def get_classes_for_lecturer(
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(get_current_user),
    get_classes_for_lecturer_use_case: GetClassesForLecturerUseCase = Depends(get_classes_for_lecturer_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_classes_for_lecturer_use_case.execute(current_user, skip, limit)
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClassesNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.post("/classes/{class_id}", response_model=schemas.Class)
def edit_class(
    request: schemas.ClassEdit,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    edit_class_use_case: EditClassUseCase = Depends(edit_class_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return edit_class_use_case.execute(request, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClassNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.delete("/classes/{class_id}", response_model=None)
def delete_class(
    class_id: int,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    delete_class_use_case: DeleteClassUseCase = Depends(delete_class_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return delete_class_use_case.execute(class_id, current_user)
    except ClassNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.get("/classes/{class_code}", response_model=schemas.Class)
def get_class(
    class_code: str,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_class_use_case: GetClassUseCase = Depends(get_class_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_class_use_case.execute(class_code, current_user)
    except ClassNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
