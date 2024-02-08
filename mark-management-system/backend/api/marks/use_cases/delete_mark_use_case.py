from typing import Tuple

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class DeleteMarkUseCase:
    """
    The Use Case containing business logic for deleting an existing mark.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository, class_repository: ClassRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.class_repository = class_repository
    
    def execute(self, mark_unique_code: str, current_user: Tuple[str, bool, bool]) -> None:
        """
        Executes the Use Case to delete an existing mark in the system.

        Args:
            mark_unique_code: The unique identifier of the mark to be deleted.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an a user & lecturer, and if the requestor is not the lecturer of the class.
            MarkNotFound: If the mark cannot be found, given the unique code.
            UserNotFound: If the user (from the JWT) cannot be found.
        """
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

        self.mark_repository.delete(mark)
