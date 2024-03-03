from typing import Tuple, List

from api.system.schemas.schemas import MarksRow

from api.marks.repositories.mark_repository import MarkRepository
from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.students.errors.student_not_found import StudentNotFound

from api.users.errors.user_not_found import UserNotFound


class GetMarksForStudentUseCase:
    """
    The Use Case containing business logic for retrieving a list of marks for a student.
    """
    def __init__(self, mark_repository: MarkRepository, student_repository: StudentRepository, user_repository: UserRepository) -> None:
        self.mark_repository = mark_repository
        self.student_repository = student_repository
        self.user_repository = user_repository
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> List[MarksRow]:
        """
        Executes the Use Case to retrieve a list of marks for a student.

        Args:
            reg_no: The unique identifier of the student. 
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an a user & lecturer, and if the requestor is not the lecturer of the class.
            MarkNotFound: If the mark cannot be found given the unique identifier.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            List[MarksRow]: A list of MarksRow schema object containing all information about the requested marks.
        """
        user_email, _, _ = current_user 

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        student = self.student_repository.find_by_reg_no(reg_no)

        if student is None:
            raise StudentNotFound("Student not found")
        
        marks = self.mark_repository.get_marks_for_student(reg_no)

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
            )

            marks_data.append(mark_row)
    
        return marks_data
