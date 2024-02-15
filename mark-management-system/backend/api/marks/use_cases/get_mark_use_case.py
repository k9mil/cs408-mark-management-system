from typing import Tuple

from api.system.schemas.schemas import Marks as MarkSchema

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetMarkUseCase:
    """
    The Use Case containing business logic for retrieving a mark from the database.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository, class_repository: ClassRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.class_repository = class_repository
    
    def execute(self, student_id: int, class_id: int, current_user: Tuple[str, bool, bool]) -> MarkSchema:
        """
        Executes the Use Case to retrieve an existing mark.

        Args:
            student_id: The student unique identifier.
            class_id: The class unique identifier.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an a user & lecturer, and if the requestor is not the lecturer of the class.
            MarkNotFound: If the mark cannot be found given the unique identifier.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            MarksSchema: A MarksSchema schema object containing all information about the requested mark.
        """
        user_email, _, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer)):
            raise PermissionError("Permission denied to access this resource")
        
        mark = self.mark_repository.find_by_student_id_and_class_id(student_id, class_id)

        if mark is None:
            raise MarkNotFound("Mark not found")
        
        is_lecturer_of_class = self.class_repository.is_lecturer_of_class(user.id, mark.class_id)

        if is_lecturer_of_class is None:
            raise PermissionError("Permission denied to access this resource")

        return mark
