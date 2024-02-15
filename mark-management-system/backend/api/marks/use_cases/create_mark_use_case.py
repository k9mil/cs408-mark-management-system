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
    """
    The Use Case containing business logic for creating a new mark.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository, class_repository: ClassRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.class_repository = class_repository

    def execute(self, request: MarksCreate, current_user: Tuple[str, bool, bool]) -> MarksSchema:
        """
        Executes the Use Case to create a new mark in the system.

        Args:
            request: A `MarksCreate` object is required which contains the necessary mark details for mark creation.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an a user & lecturer, or an administrator, and if the requestor is not the lecturer of the class.
            MarkAlreadyExists: If the mark already exists.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            MarksSchema: A MarksSchema schema object containing all information about the newly created mark.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")

        is_lecturer_of_class = self.class_repository.is_lecturer_of_class(user.id, request.class_id)

        if is_lecturer_of_class is None:
            raise PermissionError("Permission denied to access this resource")

        if self.mark_repository.find_by_student_id_and_class_id(request.student_id, request.class_id):
            raise MarkAlreadyExists("Mark already exists")

        mark = Marks(
            mark=request.mark,
            class_id=request.class_id,
            student_id=request.student_id
        )

        self.mark_repository.add(mark)

        return mark
