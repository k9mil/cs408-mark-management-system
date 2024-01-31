from typing import Tuple

from api.system.schemas.schemas import Marks as MarkSchema

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetMarkUseCase:
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository, class_repository: ClassRepository):
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.class_repository = class_repository
    
    def execute(self, mark_unique_code: str, current_user: Tuple[str, bool, bool]) -> MarkSchema:
        user_email, _, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer)):
            raise PermissionError("Permission denied to access this resource")
        
        mark = self.mark_repository.find_by_unique_code(mark_unique_code)

        if mark is None:
            raise MarkNotFound("Mark not found")
        
        is_lecturer_of_class = self.class_repository.is_lecturer_of_class(user.id, mark.class_id)

        if is_lecturer_of_class is None:
            raise PermissionError("Permission denied to access this resource")

        return mark
