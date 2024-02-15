from typing import Tuple, List

from api.system.schemas.schemas import MarksRow

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentMarksUseCase:
    """
    The Use Case containing business logic for retrieving a list of student marks from the database,
    for a particular lecturer.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
    
    def execute(self, current_user: Tuple[str, bool, bool]) -> List[MarksRow]:
        """
        Executes the Use Case to retrieve a list of marks for a lecturer.

        Args:
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an a user & lecturer, or if the user is not an administrator, and if the requestor is not the lecturer of the class.
            MarkNotFound: If no marks can be found for the lecturer.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            List[MarksRow]: A list of `MarksRow` schema object containing all information about the requested marks, and the students.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        marks = self.mark_repository.get_student_marks_for_lecturer(user.id)

        if marks is None:
            raise MarkNotFound("No results found for the lecturer")
        
        marks_row = []

        for current_mark in marks:
            mark_row = MarksRow(
                id=current_mark[0],
                student_name=current_mark[1],
                reg_no=current_mark[2],
                class_code=current_mark[3],
                degree_level=current_mark[4],
                degree_name=current_mark[5],
                mark=current_mark[6],
            )
            
            marks_row.append(mark_row)

        return marks_row
