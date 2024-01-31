from typing import Tuple

from api.system.schemas.schemas import UserEdit
from api.system.schemas.schemas import User

from api.users.repositories.user_repository import UserRepository

from api.users.hashers.bcrypt_hasher import BCryptHasher

from api.users.errors.user_not_found import UserNotFound


class EditUserUseCase:
    def __init__(self, user_repository: UserRepository, bcrypt_hasher: BCryptHasher):
        self.user_repository = user_repository
        self.bcrypt_hasher = bcrypt_hasher
    
    def execute(
            self,
            request: UserEdit,
            current_user: Tuple[str, bool, bool],
        ) -> User:
        user_email, is_admin, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not (is_admin or user.id == request.id):
            raise PermissionError("You do not have permission to change these details")
        
        self.user_repository.update(user, request, self.bcrypt_hasher)
        
        return user
