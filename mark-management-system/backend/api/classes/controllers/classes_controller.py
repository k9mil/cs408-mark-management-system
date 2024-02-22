from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple, List

from api.system.schemas import schemas

from api.classes.use_cases.create_class_use_case import CreateClassUseCase
from api.classes.use_cases.get_classes_use_case import GetClassesUseCase
from api.classes.use_cases.get_classes_for_lecturer_use_case import GetClassesForLecturerUseCase
from api.classes.use_cases.edit_class_use_case import EditClassUseCase
from api.classes.use_cases.delete_class_use_case import DeleteClassUseCase
from api.classes.use_cases.get_class_use_case import GetClassUseCase
from api.classes.use_cases.check_if_class_is_associated_with_a_degree_use_case import CheckIfClassIsAssociatedWithADegreeUseCase
from api.classes.use_cases.get_associated_degrees_for_class_use_case import GetAssociatedDegreesForClassUseCase
from api.classes.use_cases.get_class_statistics_use_case import GetClassStatisticsUseCase


from api.classes.errors.class_already_exists import ClassAlreadyExists
from api.classes.errors.classes_not_found import ClassesNotFound
from api.classes.errors.class_not_found import ClassNotFound
from api.classes.errors.class_not_associated_with_degree import ClassNotAssociatedWithDegree

from api.users.errors.user_not_found import UserNotFound

from api.degrees.errors.degree_not_found import DegreeNotFound
from api.degrees.errors.degrees_not_found import DegreesNotFound

from api.marks.errors.mark_not_found import MarkNotFound

from api.classes.dependencies import create_class_use_case
from api.classes.dependencies import get_classes_use_case
from api.classes.dependencies import get_classes_for_lecturer_use_case
from api.classes.dependencies import edit_class_use_case
from api.classes.dependencies import delete_class_use_case
from api.classes.dependencies import get_class_use_case
from api.classes.dependencies import check_if_class_is_associated_with_a_degree_use_case
from api.classes.dependencies import get_associated_degrees_for_class_use_case
from api.classes.dependencies import get_class_statistics_use_case

from api.middleware.dependencies import get_current_user


classes = APIRouter()


@classes.post("/api/v1/classes", response_model=schemas.Class)
def create_class(
    request: schemas.ClassCreate,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    create_class_use_case: CreateClassUseCase = Depends(create_class_use_case),
):
    """
    Create a new class in the system.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `request`: A `schemas.ClassCreate` object is required which contains the necessary class details for class creation.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `create_class_use_case`: The class which handles the business logic for class creation.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error, in this case, if the `is_admin` flag is false, as only administrator can create a class.  
        - `HTTPException`, 404: If the user (lecturer) in the request has not been found.  
        - `HTTPException`, 409: If the class already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Class` schema, which contains the details of the created class.  
    """
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
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.get("/api/v1/classes", response_model=List[schemas.Class])
def get_classes(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_classes_use_case: GetClassesUseCase = Depends(get_classes_use_case),
):
    """
    Retrieves a list of classes in the system.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `skip` (default: 0): A parameter which determines how many objects to skip.  
        - `limit` (default: 100): A parameter which determines the maximum amount of classes to return.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_classes_use_case`: The class which handles the business logic for class retrieval.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error, in this case, if the `is_admin` flag is false, as only administrator can create a class.  
        - `HTTPException`, 404: If no classes have been found and returned.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.Class]` schema, which returns a list of Classes.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_classes_use_case.execute(skip, limit, current_user)
    except ClassesNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@classes.get("/api/v1/classes/lecturer", response_model=List[schemas.Class])
def get_classes_for_lecturer(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_classes_for_lecturer_use_case: GetClassesForLecturerUseCase = Depends(get_classes_for_lecturer_use_case),
):
    """
    Retrieves a list of classes in the system for a particular lecturer, i.e. for the user making the request.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `skip` (default: 0): A parameter which determines how many objects to skip.  
        - `limit` (default: 100): A parameter which determines the maximum amount of classes to return.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_classes_for_lecturer_use_case`: The class which handles the business logic for class retrieval for the lecturer.  

    Raises: 
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 404: If the user has not been found (from the JWT), or if no classes have been found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.Class]` schema, which returns a list of Classes.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_classes_for_lecturer_use_case.execute(current_user, skip, limit)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClassesNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.put("/api/v1/classes/{class_id}", response_model=schemas.Class)
def edit_class(
    request: schemas.ClassEdit,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    edit_class_use_case: EditClassUseCase = Depends(edit_class_use_case),
):
    """
    Allows for editing an already existing class.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `request`: A `schemas.ClassEdit` object is which contains all of the new fields, as well as the original code & lecturer_id.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `edit_class_use_case`: The class which handles the business logic for editing the class details.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.
        - `HTTPException`, 403: If there has been a permission error, in this case, if the `is_admin` flag is false, as only administrator can create a class.  
        - `HTTPException`, 404: If the user has not been found (from the request), or if the class has not been found.  
        - `HTTPException`, 409: If the class already exists, i.e. a new code was passed in which already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Class` schema, which returns the details of the newly edited class.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return edit_class_use_case.execute(request, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClassNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClassAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.delete("/api/v1/classes/{class_id}", response_model=None)
def delete_class(
    class_id: int,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    delete_class_use_case: DeleteClassUseCase = Depends(delete_class_use_case),
):
    """
    Deletes an existing class.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `class_id`: The `class_id` of the class which is to be deleted.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `delete_class_use_case`: The class which handles the business logic for deleting the class.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error, in this case, if the `is_admin` flag is false, as only administrator can create a class.  
        - `HTTPException`, 404: If the class has not been found.  
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
        return delete_class_use_case.execute(class_id, current_user)
    except ClassNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@classes.get("/api/v1/classes/{class_code}", response_model=schemas.Class)
def get_class(
    class_code: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_class_use_case: GetClassUseCase = Depends(get_class_use_case),
):
    """
    Retrieves a particular class.    


    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `class_code`: The `class_code` of the class which is to be retrieved.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_class_use_case`: The class which handles the business logic for retrieving a class.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error, in this case, if the user making the request is not a user & a lecturer (and teaching the class) or an administrator.  
        - `HTTPException`, 404: If the user or the class have not been found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Class` schema, which returns the queried class.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_class_use_case.execute(class_code, current_user)
    except ClassNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@classes.get("/api/v1/classes/{class_code}/degree/{degree_level}/{degree_name}", response_model=schemas.ClassBase)
def check_if_class_is_associated_with_a_degree_use_case(
    class_code: str,
    degree_level: str,
    degree_name: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    check_if_class_is_associated_with_a_degree_use_case: CheckIfClassIsAssociatedWithADegreeUseCase = Depends(check_if_class_is_associated_with_a_degree_use_case),
):
    """
    Checks if a class is associated with a particular degree, as a class can be associated with many degrees.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `class_code`: The `class_code` of the class which is to be checked.  
        - `degree_level`: The `degree_level` of the degree which is to be checked against.  
        - `degree_name`: The `degree_name` of the degree which is to be checked against.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `check_if_class_is_associated_with_a_degree_use_case`: The class which handles the business logic for the check.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 404: If the class or the degree have not been found.  
        - `HTTPException`, 409: If the class is not associated with the given degree.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.ClassBase` schema, which returns bare minimum information about a class.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return check_if_class_is_associated_with_a_degree_use_case.execute(
            class_code,
            degree_level,
            degree_name,
            current_user
        )
    except ClassNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DegreeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClassNotAssociatedWithDegree as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@classes.get("/api/v1/classes/{class_code}/degrees", response_model=List[schemas.DegreeBase])
def get_associated_degrees_for_class(
    class_code: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_associated_degrees_for_class_use_case: GetAssociatedDegreesForClassUseCase = Depends(get_associated_degrees_for_class_use_case),
):
    """
    Retrieves a list of associated degrees for a particular class.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `class_code`: The `class_code` of the class.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_associated_degrees_for_class_use_case`: The class which handles the business logic for the retrieval.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 404: If the class, user or degrees have not been found.  
        - `HTTPException`, 409: If the class is not associated with the given degree.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.DegreeBase]` schema, which returns a list of the bare minimum degree information, containing the level and name.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_associated_degrees_for_class_use_case.execute(class_code, current_user)
    except ClassNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DegreesNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@classes.get("/api/v1/class/{class_code}/statistics", response_model=schemas.MarksStatistics)
def get_class_statistics(
    class_code: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_class_statistics_use_case: GetClassStatisticsUseCase = Depends(get_class_statistics_use_case),
):
    """
    Calculates statistics for a given class.

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `class_code`: The class code of the class to calculate the statistics for.
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_class_statistics_use_case`: The class which handles the business logic for the calculation of statistics for the class.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 404: If the user (lecturer) from the JWT has not been found, or if no marks have been found.
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.MarksStatistics` schema, which contains statistics such as the mean, mode and median.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_class_statistics_use_case.execute(class_code, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MarkNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
