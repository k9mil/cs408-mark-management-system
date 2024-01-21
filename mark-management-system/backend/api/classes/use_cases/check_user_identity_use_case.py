from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_not_found import UserNotFound


class CheckUserIdentityUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, lecturer_id: int, current_user: str) -> bool:
        lecturer = self.user_repository.get_user(lecturer_id)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")
        
        user = self.user_repository.find_by_email(current_user)

        if user is None:
            raise UserNotFound("User not found")
        
        is_user = (lecturer.id == user.id)

        if not is_user:
            raise PermissionError("Permission denied to access this resource")

        return is_user
