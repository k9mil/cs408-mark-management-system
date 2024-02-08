from typing import Tuple

from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_not_found import UserNotFound


class GetUserUseCase:
    """
    The Use Case containing business logic for retrieving a user.
    """
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    def execute(self, user_id: int, current_user: Tuple[str, bool, bool]) -> UserSchema:
        """
        Executes the Use Case to retrieve a user given a user_id.

        Args:
            user_id: The `user_id` of the user.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the requestor is not an administrator.
            UserNotFound: If the user is not found given the user_id.

        Returns:
            UserSchema: A UserSchema schema object containing the user details.
        """
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise UserNotFound("User not found")

        return user
