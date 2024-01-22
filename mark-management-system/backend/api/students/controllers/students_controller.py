from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple

from api.system.schemas import schemas

from api.students.use_cases.create_student_use_case import CreateStudentUseCase

from api.students.errors.student_already_exists import StudentAlreadyExists

from api.students.dependencies import create_student_use_case

from api.middleware.dependencies import get_current_user


students = APIRouter()


@students.post("/students/", response_model=schemas.Student)
def create_student(
    request: schemas.StudentCreate,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    create_student_use_case: CreateStudentUseCase = Depends(create_student_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return create_student_use_case.execute(
            request, current_user
        )
    except StudentAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
