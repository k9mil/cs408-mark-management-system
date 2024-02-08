from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple, List

from api.system.schemas import schemas

from api.marks.use_cases.create_mark_use_case import CreateMarkUseCase
from api.marks.use_cases.get_mark_use_case import GetMarkUseCase
from api.marks.use_cases.get_student_marks_use_case import GetStudentMarksUseCase
from api.marks.use_cases.get_student_statistics_use_case import GetStudentStatisticsUseCase
from api.marks.use_cases.edit_mark_use_case import EditMarkUseCase
from api.marks.use_cases.delete_mark_use_case import DeleteMarkUseCase

from api.marks.errors.mark_already_exists import MarkAlreadyExists
from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound

from api.marks.dependencies import create_mark_use_case
from api.marks.dependencies import get_mark_use_case
from api.marks.dependencies import get_student_marks_use_case
from api.marks.dependencies import get_student_statistics_use_case
from api.marks.dependencies import edit_mark_use_case
from api.marks.dependencies import delete_mark_use_case

from api.middleware.dependencies import get_current_user


marks = APIRouter()


@marks.post("/marks/", response_model=schemas.Marks)
def create_mark(
    request: schemas.MarksCreate,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    create_mark_use_case: CreateMarkUseCase = Depends(create_mark_use_case),
):
    """
    Create a new mark in the system.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `request`: A `schemas.MarksCreate` object is required which contains the necessary mark details for mark creation.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `create_mark_use_case`: The class which handles the business logic for mark creation.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found.  
        - `HTTPException`, 409: If the mark already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Marks` schema, which contains the details of the created mark.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return create_mark_use_case.execute(
            request, current_user
        )
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MarkAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.get("/marks/{mark_unique_code}", response_model=schemas.Marks)
def get_mark(
    mark_unique_code: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_mark_use_case: GetMarkUseCase = Depends(get_mark_use_case),
):
    """
    Retrieves a specific mark in the system, given a unique code.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `mark_unique_code`: The unique identifier of the mark.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_mark_use_case`: The class which handles the business logic for mark retrieval.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if the mark has not been found given the unique code.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Marks` schema, which contains the details of the retrieved mark.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_mark_use_case.execute(mark_unique_code, current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.get("/marks/", response_model=List[schemas.MarksRow])
def get_student_marks(
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_student_marks_use_case: GetStudentMarksUseCase = Depends(get_student_marks_use_case),
):
    """
    Retrieves a list of marks in the system for a particular lecturer, i.e. the requestor.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_student_marks_use_case`: The class which handles the business logic for mark retrieval per lecturer.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if no marks were found for the lecturer.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:    
        - `response_model`: The response is in the model of the `List[schemas.Marks]` schema, which contains a list of the retrieved marks.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_student_marks_use_case.execute(current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.put("/marks/{mark_unique_code}", response_model=schemas.Marks)
def edit_mark(
    request: schemas.MarksEdit,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    edit_mark_use_case: EditMarkUseCase = Depends(edit_mark_use_case),
):
    """
    Modifies an existing mark given the mark's unique code.   

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `request`: A `schemas.Marks` object is required which contains the necessary mark details for editing marks.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `edit_mark_use_case`: The class which handles the business logic for editing marks.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if a mark cannot be found given the unique code.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Marks` schema, which contains the newly modified object.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return edit_mark_use_case.execute(request, current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.delete("/marks/{mark_unique_code}", response_model=None)
def delete_mark(
    mark_unique_code: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    delete_mark_use_case: DeleteMarkUseCase = Depends(delete_mark_use_case),
):
    """
    Deletes an existing mark.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `mark_unique_code`: The `mark_unique_code` of the mark which is to be deleted. The unique identifier.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `delete_mark_use_case`: The class which handles the business logic for deleting the mark.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the mark has not been found, given the unique code.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is None.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return delete_mark_use_case.execute(
            mark_unique_code, current_user
        )
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@marks.get("/marks/statistics/", response_model=schemas.MarksStatistics)
def get_student_statistics(
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_student_statistics_use_case: GetStudentStatisticsUseCase = Depends(get_student_statistics_use_case),
):
    """
    Retrieves students statistics (mean, median, mode, pass_rate) for the classes the requestor teaches, i.e. if "John Doe" made the request,
    it would calculate the mean, median, mode, pass_rate of their uploaded marks (i.e. their students).    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        `get_student_statistics_use_case`: The class which handles the business logic for retrieving & calculating student marks.   

    Raises:  
        `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        `HTTPException`, 404: If the user from the JWT cannot be found, or if no marks are found for the lecturer.  
        `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        `response_model`: The response is in the model of the `schemas.MarksStatistics` schema, which contains the student statistics.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_student_statistics_use_case.execute(current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
