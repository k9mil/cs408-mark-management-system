from typing import Tuple

from api.system.schemas.schemas import Marks as MarkSchema

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound


class GetMarkUseCase:
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository):
        self.mark_repository = mark_repository
        self.user_repository = user_repository
    
    def execute(self, mark_unique_code: str, current_user: Tuple[str, bool]) -> MarkSchema:
        user_email, is_admin = current_user

        lecturer = self.user_repository.find_by_email(user_email)
        
        if is_admin is False or lecturer is None:
            raise PermissionError("Permission denied to access this resource")
        
        mark = self.mark_repository.find_by_unique_code(mark_unique_code)

        if mark is None:
            raise MarkNotFound("Mark not found")

        return mark
