from typing import Tuple

from api.system.schemas.schemas import Marks as MarksSchema

from api.system.schemas.schemas import MarksEdit

from api.marks.repositories.mark_repository import MarkRepository

from api.marks.errors.mark_not_found import MarkNotFound


class EditMarkUseCase:
    def __init__(self, mark_repository: MarkRepository):
        self.mark_repository = mark_repository
    
    def execute(self, request: MarksEdit, current_user: Tuple[str, bool]) -> MarksSchema:
        # _, is_admin = current_user

        # if is_admin is False:
        #     raise PermissionError("Permission denied to access this resource")

        mark = self.mark_repository.find_by_unique_code(request.unique_code)

        if mark is None:
            raise MarkNotFound("Mark not found")

        self.mark_repository.update(mark, request)

        return mark
