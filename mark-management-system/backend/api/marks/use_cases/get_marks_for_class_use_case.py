from typing import Tuple, List

from api.system.schemas.schemas import MarksRow

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetMarksForClassUseCase:
    """
    The Use Case containing business logic for retrieving marks for a class.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
    
    def execute(self, class_code: str, current_user: Tuple[str, bool, bool]) -> List[MarksRow]:
        """
        Executes the Use Case to retrieve a list of marks associated with a class.

        Args:
            class_code: The class unique identifier.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an administrator.
            MarkNotFound: If the mark cannot be found given the unique identifier.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            MarksSchema: A MarksSchema schema object containing all information about the requested mark.
        """
        user_email, is_admin, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not is_admin:
            raise PermissionError("Permission denied to access this resource")
        
        marks = self.mark_repository.get_student_marks_for_class_as_marks_row(class_code)

        if not marks:
            raise MarkNotFound("Marks not found")
        
        marks_data = []
        
        for mark in marks:
            mark_row = MarksRow(
                id=mark[0],
                student_name=mark[1],
                reg_no=mark[2],
                class_code=mark[3],
                class_name=mark[4],
                degree_level=mark[5],
                degree_name=mark[6],
                mark=mark[7],
                code=mark[8],
            )

            marks_data.append(mark_row)
    
        return marks_data
