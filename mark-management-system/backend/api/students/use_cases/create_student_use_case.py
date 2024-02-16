from typing import Tuple

from api.system.models.models import Student

from api.system.schemas.schemas import StudentCreate
from api.system.schemas.schemas import Student as StudentSchema

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.students.errors.student_already_exists import StudentAlreadyExists

from api.users.errors.user_not_found import UserNotFound


class CreateStudentUseCase:
    """
    The Use Case containing business logic for creating a new student.
    """
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository) -> None:
        self.student_repository = student_repository
        self.user_repository = user_repository

    def execute(self, request: StudentCreate, current_user: Tuple[str, bool, bool]) -> StudentSchema:
        """
        Executes the Use Case to create a new student in the system.

        Args:
            request: A `StudentCreate` object is required which contains the necessary student details for student creation.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not a user and a lecturer, or an administrator.
            StudentAlreadyExists: If the student already exists.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            StudentSchema: A StudentSchema schema object containing all information about the newly created student.
        """
        user_email, is_admin, is_lecturer = current_user

        # TODO: temporarily lecturers can create students, i.e. when they upload marks.

        user = self.user_repository.find_by_email(user_email)
        
        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        if self.student_repository.find_by_reg_no(request.reg_no):
            raise StudentAlreadyExists("Student already exists")

        student = Student(
            reg_no=request.reg_no,
            student_name=request.student_name,
            degree_id=request.degree_id,
        )

        self.student_repository.add(student)

        return student
