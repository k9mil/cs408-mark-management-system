from typing import Tuple

from api.system.models.models import RoleUsers

from api.system.schemas.schemas import RoleUsersData

from api.roles.repositories.roles_repository import RolesRepository

from api.users.repositories.user_repository import UserRepository

from api.roles.errors.role_not_found import RoleNotFound
from api.roles.errors.role_association_already_exists import RoleAssociationAlreadyExists

from api.users.errors.user_not_found import UserNotFound


class AddUserToRoleUseCase:
    def __init__(self, roles_repository: RolesRepository, user_repository: UserRepository):
        self.roles_repository = roles_repository
        self.user_repository = user_repository

    def execute(self, request: RoleUsersData, current_user: Tuple[str, bool]) -> RoleUsersData:
        _, is_admin = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        user = self.user_repository.find_by_id(request.user_id)

        if user is None:
            raise UserNotFound("User not found.")

        role = self.roles_repository.find_by_id(request.role_id)

        if role is None:
            raise RoleNotFound("Role not found.")
        
        user_role = self.roles_repository.find_role_association(request)

        if user_role is not None:
            raise RoleAssociationAlreadyExists("Role association already exists.")

        role_user = RoleUsers(
            user_id=request.user_id,
            role_id=request.role_id
        )

        self.roles_repository.add_user(role_user, user)

        return role_user