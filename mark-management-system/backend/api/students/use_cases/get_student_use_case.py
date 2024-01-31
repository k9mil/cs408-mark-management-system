from typing import Tuple

from api.system.schemas.schemas import Student as StudentSchema

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.students.errors.student_not_found import StudentNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentUseCase:
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> StudentSchema:
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
