from fastapi import Depends, APIRouter, HTTPException, Body

from typing import Tuple, List

from api.system.schemas import schemas

from api.degrees.use_cases.create_degree_use_case import CreateDegreeUseCase
from api.degrees.use_cases.get_degree_use_case import GetDegreeUseCase
from api.degrees.use_cases.get_degrees_use_case import GetDegreesUseCase

from api.degrees.errors.degree_already_exists import DegreeAlreadyExists
from api.degrees.errors.degree_not_found import DegreeNotFound

from api.users.errors.user_not_found import UserNotFound

from api.degrees.dependencies import create_degree_use_case
from api.degrees.dependencies import get_degree_use_case
from api.degrees.dependencies import get_degrees_use_case

from api.middleware.dependencies import get_current_user


degrees = APIRouter()


@degrees.post("/api/v1/degrees", response_model=schemas.Degree)
def create_degree(
    request: schemas.DegreeCreate,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    create_degree_use_case: CreateDegreeUseCase = Depends(create_degree_use_case),
):
    """
    Create a new degree in the system.

    Args:  
        - `request`: A `schemas.DegreeCreate` object is required which contains the necessary degree details for degree creation.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `create_degree_use_case`: The class which handles the business logic for degree creation.   

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error, in this case, if the `is_admin` flag is false, as only administrator can create a degree.  
        - `HTTPException`, 409: If the degree already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Degree` schema, which contains the details of the created degree.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return create_degree_use_case.execute(
            request, current_user
        )
    except DegreeAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@degrees.get("/api/v1/degrees/{degree_name}", response_model=schemas.Degree)
def get_degree(
    degree_name: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_degree_use_case: GetDegreeUseCase = Depends(get_degree_use_case),
):
    """
    Retrieves a particular degree.

    Args:  
        - `degree_name`: The `degree_name` of the degree which is to be retrieved.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_degree_use_case`: The class which handles the business logic for retrieving a degree.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error and the user making the request is not authorised to make this request.  
        - `HTTPException`, 404: If the user or the degree have not been found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.Degree` schema, which returns the queried degree.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_degree_use_case.execute(degree_name, current_user)
    except DegreeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@degrees.post("/api/v1/degrees/search", response_model=List[schemas.Degree])
def get_degrees(
    degrees: List[schemas.DegreeBase] = Body(...), 
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_degrees_use_case: GetDegreesUseCase = Depends(get_degrees_use_case),
):
    """
    Search for degrees based on a particular criteria, i.e. checks if they exist in bulk.

    Args:  
        - `degrees`: A list in the form of DegreeBase (level: str, name: str) objects to be searched.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_degrees_use_case`: The class which handles the business logic for searching.  

    Raises:  
        - `HTTPException`, 400: If the body passed in is empty, i.e. no degree details are provided.  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error and the user making the request is not authorised to make this request.  
        - `HTTPException`, 404: If the user or any of the degrees have not been found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.Degree]` schema, which returns a list of the degrees, but with more information than passed in.  
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )   

    if len(degrees) == 0:
        raise HTTPException(
            status_code=400,
            detail="Degree details are required"
        ) 

    try:
        return get_degrees_use_case.execute(degrees, current_user)
    except DegreeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
