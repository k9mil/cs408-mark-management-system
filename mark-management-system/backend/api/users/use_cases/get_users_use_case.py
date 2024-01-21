from typing import Tuple

from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.users_not_found import UsersNotFound


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, skip: int, limit: int, current_user: Tuple[str, bool]) -> list[UserSchema]:
        _, is_admin = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        users = self.user_repository.get_users(skip, limit)

        if users is None:
            raise UsersNotFound("Users not found")

        return users
