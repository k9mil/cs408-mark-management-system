from fastapi import Depends, APIRouter, HTTPException

from typing import Tuple

from api.system.schemas import schemas

from api.roles.use_cases.add_user_to_role_use_case import AddUserToRoleUseCase
from api.roles.use_cases.remove_user_from_role_use_case import RemoveUserFromRoleUseCase

from api.roles.errors.role_not_found import RoleNotFound
from api.roles.errors.role_association_already_exists import RoleAssociationAlreadyExists
from api.roles.errors.role_association_not_found import RoleAssociationNotFound

from api.users.errors.user_not_found import UserNotFound

from api.roles.dependencies import add_user_to_role_use_case
from api.roles.dependencies import remove_user_from_role_use_case

from api.middleware.dependencies import get_current_user


roles = APIRouter()


@roles.post("/roles/add_user", response_model=schemas.RoleUsers)
def add_user_to_role(
    request: schemas.RoleUsersData,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    add_user_to_role_use_case: AddUserToRoleUseCase = Depends(add_user_to_role_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )
    
    try:
        return add_user_to_role_use_case.execute(
            request, current_user
        )
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except RoleNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except RoleAssociationAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@roles.post("/roles/remove_user", response_model=schemas.RoleUsers)
def remove_user_from_role(
    request: schemas.RoleUsersData,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    remove_user_from_role_use_case: RemoveUserFromRoleUseCase = Depends(remove_user_from_role_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )
    
    try:
        return remove_user_from_role_use_case.execute(
            request, current_user
        )
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except RoleNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except RoleAssociationNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
