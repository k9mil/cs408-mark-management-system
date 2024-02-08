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


@roles.post("/roles/{role_id}/user/{user_id}", response_model=schemas.RoleUsers)
def add_user_to_role(
    request: schemas.RoleUsersData,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    add_user_to_role_use_case: AddUserToRoleUseCase = Depends(add_user_to_role_use_case),
):
    """
    Adds a user to a role, given a role_id and user_id.

    Args:
        request: A `schemas.RoleUsersData` object which contains the role_id of the role, and the user_id of the user.
        current_user: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean. 
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.
        add_user_to_role_use_case: The class which handles the business logic for adding a user to a role. 

    Raises:
        HTTPException, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.
        HTTPException, 403: If there has been a permission error, in this case, if the `is_admin` flag is false, as only administrator can create a assign roles to users.
        HTTPException, 404: If the user (lecturer) in the request has not been found, or is the role has not been found.
        HTTPException, 409: If the role association already exists, i.e. if the given user already has the given role.
        HTTPException, 500: If any other system exception occurs.

    Returns:
        response_model: The response is in the model of the `schemas.RoleUsers` schema, which contains the user_id, role_id and an integer of the object.
    """
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
        raise HTTPException(status_code=404, detail=str(e))
    except RoleNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoleAssociationAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@roles.delete("/roles/{role_id}/user/{user_id}", response_model=None)
def remove_user_from_role(
    request: schemas.RoleUsersData,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    remove_user_from_role_use_case: RemoveUserFromRoleUseCase = Depends(remove_user_from_role_use_case),
):
    """
    Removes a user to a role, given a role_id and user_id.

    Args:
        request: A `schemas.RoleUsersData` object which contains the role_id of the role, and the user_id of the user.
        current_user: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean. 
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.
        remove_user_from_role_use_case: The class which handles the business logic for removing a user from a role.

    Raises:
        HTTPException, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.
        HTTPException, 403: If there has been a permission error, in this case, if the `is_admin` flag is false, as only administrator can remove an assigned role from users.
        HTTPException, 404: If the user (lecturer) in the request has not been found, if is the role has not been found, or if the role association between the user and role is not found.
        HTTPException, 500: If any other system exception occurs.
    """
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
        raise HTTPException(status_code=404, detail=str(e))
    except RoleNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoleAssociationNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    