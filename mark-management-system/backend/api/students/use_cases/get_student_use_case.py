from typing import Tuple

from api.system.schemas.schemas import Student as StudentSchema

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.students.errors.student_not_found import StudentNotFound


class GetStudentUseCase:
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository
    
    def execute(self, student_id: int, current_user: Tuple[str, bool]) -> StudentSchema:
        user_email, is_admin = current_user

        lecturer = self.user_repository.find_by_email(user_email)
        
        if is_admin is False or lecturer is None:
            raise PermissionError("Permission denied to access this resource")
        
        student = self.student_repository.find_by_id(student_id)

        if student is None:
            raise StudentNotFound("Student not found")

        return student
