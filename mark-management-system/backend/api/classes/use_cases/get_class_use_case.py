from typing import Tuple

from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.class_not_found import ClassNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, class_code: str, current_user: Tuple[str, bool, bool]) -> ClassSchema:
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)
        
        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        class_ = self.class_repository.find_by_code(class_code)

        if class_ is None:
            raise ClassNotFound("Class not found")
        
        if class_.lecturer_id != user.id:
            raise PermissionError("Permission denied to access this resource")

        return class_
