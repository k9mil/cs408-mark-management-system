from typing import Tuple

from api.system.models.models import Marks

from api.system.schemas.schemas import MarksCreate
from api.system.schemas.schemas import Marks as MarksSchema

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository

from api.marks.errors.mark_already_exists import MarkAlreadyExists

from api.users.errors.user_not_found import UserNotFound


class CreateMarkUseCase:
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository, class_repository: ClassRepository):
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.class_repository = class_repository

    def execute(self, request: MarksCreate, current_user: Tuple[str, bool, bool]) -> MarksSchema:
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")

        is_lecturer_of_class = self.class_repository.is_lecturer_of_class(user.id, request.class_id)

        if is_lecturer_of_class is None:
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
