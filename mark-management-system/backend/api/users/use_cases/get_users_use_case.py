from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.users_not_found import UsersNotFound


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, skip: int, limit: int) -> list[UserSchema]:
        users = self.user_repository.get_users(skip, limit)

        if users is None:
            raise UsersNotFound("Users not found")

        return users
