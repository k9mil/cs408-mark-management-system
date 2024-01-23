from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple, List

from api.system.schemas import schemas

from api.marks.use_cases.create_mark_use_case import CreateMarkUseCase
from api.marks.use_cases.get_mark_use_case import GetMarkUseCase

from api.marks.errors.mark_already_exists import MarkAlreadyExists
from api.marks.errors.mark_not_found import MarkNotFound

from api.marks.dependencies import create_mark_use_case
from api.marks.dependencies import get_mark_use_case
from api.marks.dependencies import get_student_marks_use_case

from api.middleware.dependencies import get_current_user


marks = APIRouter()


@marks.post("/marks/", response_model=schemas.Marks)
def create_mark(
    request: schemas.MarksCreate,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    create_mark_use_case: CreateMarkUseCase = Depends(create_mark_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return create_mark_use_case.execute(
            request, current_user
        )
    except MarkAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.get("/marks/{mark_unique_code}", response_model=schemas.Marks)
def get_mark(
    mark_unique_code: str,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_mark_use_case: GetMarkUseCase = Depends(get_mark_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_mark_use_case.execute(mark_unique_code, current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.get("/marks/", response_model=List[schemas.MarksRow])
def get_student_marks(
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_student_marks_use_case: GetMarkUseCase = Depends(get_student_marks_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_student_marks_use_case.execute(current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
