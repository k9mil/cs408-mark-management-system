from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple, List

from api.system.schemas import schemas

from api.marks.use_cases.create_mark_use_case import CreateMarkUseCase
from api.marks.use_cases.get_mark_use_case import GetMarkUseCase
from api.marks.use_cases.get_student_marks_use_case import GetStudentMarksUseCase
from api.marks.use_cases.get_student_statistics_use_case import GetStudentStatisticsUseCase
from api.marks.use_cases.edit_mark_use_case import EditMarkUseCase
from api.marks.use_cases.delete_mark_use_case import DeleteMarkUseCase
from api.marks.use_cases.get_marks_for_student_use_case import GetMarksForStudentUseCase
from api.marks.use_cases.get_marks_for_class_use_case import GetMarksForClassUseCase
from api.marks.use_cases.get_global_student_statistics_use_case import GetGlobalStudentStatisticsUseCase

from api.marks.errors.mark_already_exists import MarkAlreadyExists
from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound

from api.students.errors.student_not_found import StudentNotFound

from api.marks.dependencies import create_mark_use_case
from api.marks.dependencies import get_mark_use_case
from api.marks.dependencies import get_student_marks_use_case
from api.marks.dependencies import get_student_statistics_use_case
from api.marks.dependencies import edit_mark_use_case
from api.marks.dependencies import delete_mark_use_case
from api.marks.dependencies import get_marks_for_student_use_case
from api.marks.dependencies import get_marks_for_class_use_case
from api.marks.dependencies import get_global_student_statistics_use_case

from api.middleware.dependencies import get_current_user


marks = APIRouter()


@marks.post("/api/v1/marks", response_model=schemas.Marks)
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

@marks.get("/api/v1/marks/{student_id}/{class_id}", response_model=schemas.Marks)
def get_mark(
    student_id: int,
    class_id: int,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_mark_use_case: GetMarkUseCase = Depends(get_mark_use_case),
):
    """
    Retrieves a specific mark in the system, given a student_id and a class_id.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `student_id`: The unique identifier of the student to retrieve the mark from.  
        - `class_id`: The unique identifier of the class.
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_mark_use_case`: The class which handles the business logic for mark retrieval.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if the mark has not been found given the mark identifier.  
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
        return get_mark_use_case.execute(student_id, class_id, current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.get("/api/v1/marks", response_model=List[schemas.MarksRow])
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

@marks.put("/api/v1/marks/{mark_id}", response_model=schemas.Marks)
def edit_mark(
    request: schemas.MarksEdit,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    edit_mark_use_case: EditMarkUseCase = Depends(edit_mark_use_case),
):
    """
    Modifies an existing mark given the mark's identifier.   

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
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if a mark cannot be found given the identifier.  
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

@marks.delete("/api/v1/marks/{mark_id}", response_model=None)
def delete_mark(
    mark_id: int,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    delete_mark_use_case: DeleteMarkUseCase = Depends(delete_mark_use_case),
):
    """
    Deletes an existing mark.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `mark_id`: The `mark_id` of the mark which is to be deleted. The unique identifier.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `delete_mark_use_case`: The class which handles the business logic for deleting the mark.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the mark has not been found, given the unique identifier.  
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
            mark_id, current_user
        )
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@marks.get("/api/v1/marks/statistics", response_model=schemas.MarksStatistics)
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
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_student_statistics_use_case`: The class which handles the business logic for retrieving & calculating student marks.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if no marks are found for the lecturer.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.MarksStatistics` schema, which contains the student statistics.
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
    
@marks.get("/api/v1/marks/global/statistics/all", response_model=schemas.MarksStatistics)
def get_global_student_statistics(
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_global_student_statistics_use_case: GetGlobalStudentStatisticsUseCase = Depends(get_global_student_statistics_use_case),
):
    """
    Retrieves students statistics (mean, median, mode, pass_rate) for every uploaded mark in the system.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_global_student_statistics_use_case`: The class which handles the business logic for retrieving & calculating student marks.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if no marks are found for the lecturer.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.MarksStatistics` schema, which contains the student statistics.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_global_student_statistics_use_case.execute(current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.get("/api/v1/marks/{reg_no}", response_model=List[schemas.MarksRow])
def get_marks_for_student(
    reg_no: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_marks_for_student_use_case: GetMarksForStudentUseCase = Depends(get_marks_for_student_use_case),
):
    """
    Retrieves all the marks for a given student.

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `reg_no`: The unique identifier of the student. 
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_marks_for_student_use_case`: The class which handles the business logic for mark retrieval for the student.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, if the student is not found or if no marks are found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.MarksRow]` schema, which contains the details of the retrieved marks amongst other details.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_marks_for_student_use_case.execute(reg_no, current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except StudentNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@marks.get("/api/v1/marks/class/{class_code}/all", response_model=List[schemas.MarksRow])
def get_marks_for_class(
    class_code: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_marks_for_class_use_case: GetMarksForClassUseCase = Depends(get_marks_for_class_use_case),
):
    """
    Retrieves a list of marks associated with/uploaded for a class. 

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `class_code`: The unique identifier of the class.
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_marks_for_class_use_case`: The class which handles the business logic for mark retrieval.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user from the JWT cannot be found, or if no marks are found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.MarksRow]` schema, which contains the details of the retrieved marks for the class.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_marks_for_class_use_case.execute(class_code, current_user)
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
