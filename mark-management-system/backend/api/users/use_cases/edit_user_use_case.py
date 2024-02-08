from typing import Tuple

from api.system.schemas.schemas import UserEdit
from api.system.schemas.schemas import User

from api.users.repositories.user_repository import UserRepository

from api.users.hashers.bcrypt_hasher import BCryptHasher

from api.users.errors.user_not_found import UserNotFound


class EditUserUseCase:
    """
    The Use Case containing business logic for editing an exiting user.
    """
    def __init__(self, user_repository: UserRepository, bcrypt_hasher: BCryptHasher) -> None:
        self.user_repository = user_repository
        self.bcrypt_hasher = bcrypt_hasher
    
    def execute(
            self,
            request: UserEdit,
            current_user: Tuple[str, bool, bool],
        ) -> User:
        """
        Executes the Use Case to edit an existing user in the system.

        Args:
            request: A `UserEdit` object is which contains all of the new fields which will replace the existing ones.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an administrator or if the user making the request is not the id in the request (i.e. if they are not who they claim to be).
            UserNotFound: If the user (from the JWT) is not found.

        Returns:
            User: A User schema object containing all information about the newly edited user.
        """
        user_email, is_admin, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not (is_admin or user.id == request.id):
            raise PermissionError("You do not have permission to change these details")
        
        self.user_repository.update(user, request, self.bcrypt_hasher)
        
        return user
