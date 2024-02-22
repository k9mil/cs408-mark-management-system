from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple, List

from api.system.schemas import schemas

from api.students.use_cases.create_student_use_case import CreateStudentUseCase
from api.students.use_cases.get_student_use_case import GetStudentUseCase
from api.students.use_cases.get_students_use_case import GetStudentsUseCase
from api.students.use_cases.get_student_statistics_use_case import GetStudentStatisticsUseCase

from api.students.errors.student_already_exists import StudentAlreadyExists
from api.students.errors.student_not_found import StudentNotFound

from api.users.errors.user_not_found import UserNotFound

from api.marks.errors.mark_not_found import MarkNotFound

from api.students.dependencies import create_student_use_case
from api.students.dependencies import get_student_use_case
from api.students.dependencies import get_students_use_case
from api.students.dependencies import get_student_statistics_use_case

from api.middleware.dependencies import get_current_user


students = APIRouter()


@students.post("/api/v1/students", response_model=schemas.Student)
def create_student(
    request: schemas.StudentCreate,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    create_student_use_case: CreateStudentUseCase = Depends(create_student_use_case),
):
    """
    Create a new student in the system.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `request`: A `schemas.StudentCreate` object is required which contains the necessary student details for student creation.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `create_student_use_case`: The class which handles the business logic for student creation.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user (lecturer) from the JWT has not been found.  
        - `HTTPException`, 409: If the student already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Student` schema, which contains the details of the created student.
    """
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
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@students.get("/api/v1/students/{reg_no}", response_model=schemas.Student)
def get_student(
    reg_no: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_student_use_case: GetStudentUseCase = Depends(get_student_use_case),
):
    """
    Retrieves a student from the system given a registration number.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `reg_no`: The registration number of the user to retrieve.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_student_use_case`: The class which handles the business logic for student retrieval.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user (lecturer) from the JWT has not been found, or if the student is not found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Student` schema, which contains the details of the retrievied student.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_student_use_case.execute(reg_no, current_user)
    except StudentNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@students.get("/api/v1/students", response_model=List[schemas.StudentBase])
def get_students(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_students_use_case: GetStudentsUseCase = Depends(get_students_use_case),
):
    """
    Retrieves all students from the system. 

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:
        - `skip` (default: 0): A parameter which determines how many objects to skip.  
        - `limit` (default: 100): A parameter which determines the maximum amount of users to return.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_students_use_case`: The class which handles the business logic for retrieving all students.

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user (lecturer) from the JWT has not been found, or if the student is not found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.StudentBase` schema, which contains a limited amount of information about the student.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_students_use_case.execute(skip, limit, current_user)
    except StudentNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@students.get("/api/v1/students/{reg_no}/statistics", response_model=schemas.StudentStatistics)
def get_student_statistics(
    reg_no: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_student_statistics_use_case: GetStudentStatisticsUseCase = Depends(get_student_statistics_use_case),
):
    """
    Retrieves a student from the system given a registration number alongside their statistics. 

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `reg_no`: The registration number of the user to retrieve.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_student_statistics_use_case`: The class which handles the business logic for the calculation of student statistics.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 404: If the user (lecturer) from the JWT has not been found, or if no marks have been found.
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.StudentStatistics` schema, which contains statistics such as their mean, mode and median.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_student_statistics_use_case.execute(reg_no, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
