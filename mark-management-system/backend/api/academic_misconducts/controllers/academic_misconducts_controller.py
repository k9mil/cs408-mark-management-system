from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple, List

from api.system.schemas import schemas

from api.academic_misconducts.use_cases.create_academic_misconduct_use_case import CreateAcademicMisconductUseCase

from api.academic_misconducts.errors.academic_misconducts_already_exist import AcademicMisconductsAreadyExist
from api.academic_misconducts.errors.academic_misconducts_not_found import AcademicMisconductNotFound

from api.users.errors.user_not_found import UserNotFound

from api.classes.errors.class_not_found import ClassNotFound

from api.students.errors.student_not_found import StudentNotFound

from api.middleware.dependencies import get_current_user

from api.academic_misconducts.dependencies import create_academic_misconduct_use_case


academic_misconducts = APIRouter()


@academic_misconducts.post("/api/v1/academic-misconducts", response_model=schemas.AcademicMisconductBase)
def create_academic_misconduct(
    request: schemas.AcademicMisconductCreate,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    create_academic_misconduct_use_case: CreateAcademicMisconductUseCase = Depends(create_academic_misconduct_use_case),
):
    """
    Create a new academic misconduct entry in the system for a user and class combination.

    Args:  
        - `request`: A `schemas.AcademicMisconductBase` object is required which contains the academic misconduct details, as well as the student & class to which this will be assigned to.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `create_academic_misconduct_use_case`: The class which handles the business logic for academic misconduct creation.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if the student, or the class from the request is not found.  
        - `HTTPException`, 409: If the academic misconduct already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.AcademicMisconductBase` schema, which contains the details of the created academic misconduct.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return create_academic_misconduct_use_case.execute(
            request, current_user
        )
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except StudentNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClassNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AcademicMisconductsAreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
