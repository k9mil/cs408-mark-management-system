from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple, List

from api.system.schemas import schemas

from api.personal_circumstances.use_cases.create_personal_circumstance_use_case import CreatePersonalCircumstanceUseCase
from api.personal_circumstances.use_cases.get_personal_circumstances_for_student_use_case import GetPersonalCircumstancesForStudentUseCase

from api.personal_circumstances.errors.personal_circumstances_already_exist import PersonalCircumstanceAlreadyExists
from api.personal_circumstances.errors.personal_circumstances_not_found import PersonalCircumstanceNotFound

from api.users.errors.user_not_found import UserNotFound

from api.middleware.dependencies import get_current_user

from api.personal_circumstances.dependencies import create_personal_circumstance_use_case
from api.personal_circumstances.dependencies import get_personal_circumstances_for_student_use_case


personal_circumstances = APIRouter()

@personal_circumstances.post("/personal-circumstances/", response_model=schemas.PersonalCircumstancesBase)
def create_personal_circumstance(
    request: schemas.PersonalCircumstancesCreate,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    create_personal_circumstance_use_case: CreatePersonalCircumstanceUseCase = Depends(create_personal_circumstance_use_case),
):
    """
    Create a new personal circumstances in the system for a specific user.

    Args:  
        - `request`: A `schemas.PersonalCircumstancesCreate` object is required which contains the personal circumstance details, as well as the student to which this will be assigned to.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `create_personal_circumstance_use_case`: The class which handles the business logic for personal circumstances creation.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 409: If the personal circumstance already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.PersonalCircumstancesBase` schema, which contains the details of the created personal circumstances.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return create_personal_circumstance_use_case.execute(
            request, current_user
        )
    except PersonalCircumstanceAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@personal_circumstances.get("/personal-circumstances/{reg_no}", response_model=List[schemas.PersonalCircumstancesBase])
def get_personal_circumstances_for_student(
    reg_no: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_personal_circumstances_for_student_use_case: GetPersonalCircumstancesForStudentUseCase = Depends(get_personal_circumstances_for_student_use_case),
):
    """
    Retrieves all the personal circumstances for a given student.

    Args:  
        - `reg_no`: The unique identifier of the student.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `create_personal_circumstance_use_case`: The class which handles the business logic for personal circumstances creation.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If the requestor doesn't have the required permissions.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or the personal circumstances aren't found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.PersonalCircumstancesBase]` schema, which containsa list cotaining details of the personal circumstances.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_personal_circumstances_for_student_use_case.execute(
            reg_no, current_user
        )
    except PersonalCircumstanceNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
