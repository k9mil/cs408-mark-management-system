from fastapi import Depends

from api.roles.repositories.roles_repository import RolesRepository
from api.users.repositories.user_repository import UserRepository

from api.roles.use_cases.add_user_to_role_use_case import AddUserToRoleUseCase
from api.roles.use_cases.remove_user_from_role_use_case import RemoveUserFromRoleUseCase


from api.middleware.dependencies import get_roles_repository
from api.middleware.dependencies import get_user_repository


def add_user_to_role_use_case(
        roles_repository: RolesRepository = Depends(get_roles_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> AddUserToRoleUseCase:
    return AddUserToRoleUseCase(
        roles_repository, 
        user_repository
    )

def remove_user_from_role_use_case(
        roles_repository: RolesRepository = Depends(get_roles_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> RemoveUserFromRoleUseCase:
    return RemoveUserFromRoleUseCase(
        roles_repository, 
        user_repository
    )
