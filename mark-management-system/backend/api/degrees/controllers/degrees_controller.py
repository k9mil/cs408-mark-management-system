from fastapi import Depends, APIRouter, HTTPException, Query

from typing import Tuple, List, Annotated

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


@degrees.post("/degrees/", response_model=schemas.Degree)
def create_degree(
    request: schemas.DegreeCreate,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    create_degree_use_case: CreateDegreeUseCase = Depends(create_degree_use_case),
):
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

@degrees.get("/degrees/{degree_name}", response_model=schemas.Degree)
def get_degree(
    degree_name: str,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_degree_use_case: GetDegreeUseCase = Depends(get_degree_use_case),
):
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
    
@degrees.get("/degrees/", response_model=List[schemas.Degree])
def get_degrees(
    degree_names: Annotated[List[str], Query()] = [],
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_degrees_use_case: GetDegreesUseCase = Depends(get_degrees_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )   

    if len(degree_names) == 0:
        raise HTTPException(
            status_code=400,
            detail="Degree names are required"
        ) 

    try:
        return get_degrees_use_case.execute(degree_names, current_user)
    except DegreeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
