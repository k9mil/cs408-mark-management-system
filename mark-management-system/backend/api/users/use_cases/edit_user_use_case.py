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
            current_user: Tuple[str, bool],
        ) -> User:
        user = self.user_repository.find_by_email(current_user[0])

        if user is None:
            raise UserNotFound("User not found")
        
        if user.id != request.id:
            raise Exception("You can only change details for yourself")
        
        self.user_repository.update(user, request, self.bcrypt_hasher)
        
        return user
