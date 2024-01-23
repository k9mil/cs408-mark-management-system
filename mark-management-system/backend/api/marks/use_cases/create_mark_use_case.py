from typing import Tuple

from api.system.models.models import Marks

from api.system.schemas.schemas import MarksCreate
from api.system.schemas.schemas import Marks as MarksSchema

from api.marks.repositories.mark_repository import MarkRepository

from api.marks.errors.mark_already_exists import MarkAlreadyExists


class CreateMarkUseCase:
    def __init__(self, mark_repository: MarkRepository):
        self.mark_repository = mark_repository

    def execute(self, request: MarksCreate, current_user: Tuple[str, bool]) -> MarksSchema:
        _, is_admin = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        if self.mark_repository.find_by_unique_code(request.unique_code):
            raise MarkAlreadyExists("Mark already exists")

        mark = Marks(
            unique_code=request.unique_code,
            mark=request.mark,
            class_id=request.class_id,
            student_id=request.student_id
        )

        self.mark_repository.add(mark)

        return mark
