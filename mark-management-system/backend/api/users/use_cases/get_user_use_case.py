from typing import Tuple

from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_not_found import UserNotFound


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int, current_user: Tuple[str, bool, bool]) -> UserSchema:
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise UserNotFound("User not found")

        return user
