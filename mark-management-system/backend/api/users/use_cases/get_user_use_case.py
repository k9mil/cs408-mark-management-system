from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_not_found import UserNotFound


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> UserSchema:
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise UserNotFound("User not found")

        return user
