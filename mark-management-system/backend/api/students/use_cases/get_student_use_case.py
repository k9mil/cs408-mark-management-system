from typing import Tuple

from api.system.schemas.schemas import Student as StudentSchema

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.students.errors.student_not_found import StudentNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentUseCase:
    """
    The Use Case containing business logic for retrieving a new student.
    """
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository) -> None:
        self.student_repository = student_repository
        self.user_repository = user_repository
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> StudentSchema:
        """
        Executes the Use Case to retrieve a student from the system, given a registration number.

        Args:
            reg_no: The unique identifier for the student, the registration number.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not a user and a lecturer, or an administrator.
            StudentNotFound: If the student cannot be found, given the identifier.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            StudentSchema: A StudentSchema schema object containing all information about the student.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)
        
        if user is None:
            raise UserNotFound("User not found")

        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        student = self.student_repository.find_by_reg_no(reg_no)

        if student is None:
            raise StudentNotFound("Student not found")

        return student
