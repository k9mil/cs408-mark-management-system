from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple

from api.system.schemas import schemas

from api.degrees.use_cases.create_degree_use_case import CreateDegreeUseCase
from api.degrees.use_cases.get_degree_use_case import GetDegreeUseCase

from api.degrees.errors.degree_already_exists import DegreeAlreadyExists
from api.degrees.errors.degree_not_found import DegreeNotFound

from api.degrees.dependencies import create_degree_use_case
from api.degrees.dependencies import get_degree_use_case

from api.middleware.dependencies import get_current_user


degrees = APIRouter()


@degrees.post("/degrees/", response_model=schemas.Degree)
def create_degree(
    request: schemas.DegreeCreate,
    current_user: Tuple[str, bool] = Depends(get_current_user),
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
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@degrees.get("/degrees/{degree_id}", response_model=None)
def get_degree(
    degree_id: int,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_degree_use_case: GetDegreeUseCase = Depends(get_degree_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )    

    try:
        return get_degree_use_case.execute(degree_id, current_user)
    except DegreeNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
