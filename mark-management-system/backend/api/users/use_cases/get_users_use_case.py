from typing import Tuple, List

from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.users_not_found import UsersNotFound


class GetUsersUseCase:
    """
    The Use Case containing business logic for retrieving a list of users.
    """
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    def execute(self, skip: int, limit: int, current_user: Tuple[str, bool, bool]) -> List[UserSchema]:
        """
        Executes the Use Case to retrieve a list of users.

        Args:
            skip: The amount to skip.
            limit: The maximum number of items to be retrieved.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.
        
        Raises:
            PermissionError: If the requestor is not an administrator.
            UsersNotFound: If no users are returned from the repository.

        Returns:
            List[UserSchema]: A list of `UserSchema` objects, containing the information about the users.
        """
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        users = self.user_repository.get_users(skip, limit)

        if users is None:
            raise UsersNotFound("Users not found")

        return users
