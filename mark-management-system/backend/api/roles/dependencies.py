from fastapi import Depends

from sqlalchemy.orm import Session

from api.database import get_db

from api.roles.repositories.roles_repository import RolesRepository
from api.users.repositories.user_repository import UserRepository

from api.roles.use_cases.add_user_to_role_use_case import AddUserToRoleUseCase
from api.roles.use_cases.remove_user_from_role_use_case import RemoveUserFromRoleUseCase


def get_roles_repository(db: Session = Depends(get_db)) -> RolesRepository:
    return RolesRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

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
