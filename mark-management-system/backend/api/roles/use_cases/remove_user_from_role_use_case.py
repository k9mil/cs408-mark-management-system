from typing import Tuple

from api.system.schemas.schemas import RoleUsersData

from api.roles.repositories.roles_repository import RolesRepository
from api.users.repositories.user_repository import UserRepository

from api.roles.errors.role_not_found import RoleNotFound
from api.roles.errors.role_association_not_found import RoleAssociationNotFound

from api.users.errors.user_not_found import UserNotFound


class RemoveUserFromRoleUseCase:
    """
    The Use Case containing business logic for removing a user from a particular role.
    """
    def __init__(self, roles_repository: RolesRepository, user_repository: UserRepository) -> None:
        self.roles_repository = roles_repository
        self.user_repository = user_repository

    def execute(self, request: RoleUsersData, current_user: Tuple[str, bool, bool]) -> None:
        """
        Executes the Use Case to remove a user from a role.

        Args:
            request: A `RoleUsersData` object which contains the role_id of the role, and the user_id of the user.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user (from the request) cannot be found.
            RoleNotFound: If the role (from the request) cannot be found.
            RoleAssociationNotFound: If the given user does not have the given role.
        """
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        user = self.user_repository.find_by_id(request.user_id)

        if user is None:
            raise UserNotFound("User not found.")

        role = self.roles_repository.find_by_id(request.role_id)

        if role is None:
            raise RoleNotFound("Role not found.")
        
        user_role = self.roles_repository.find_role_association(request)

        if user_role is None:
            raise RoleAssociationNotFound("Role association not found.")

        self.roles_repository.remove_user(user_role, user)
