from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple

from api.system.schemas import schemas

from api.degrees.use_cases.create_degree_use_case import CreateDegreeUseCase

from api.degrees.errors.degree_already_exists import DegreeAlreadyExists

from api.degrees.dependencies import create_degree_use_case

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
