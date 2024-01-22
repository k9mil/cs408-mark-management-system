from typing import Tuple

from api.system.models.models import Student

from api.system.schemas.schemas import StudentCreate
from api.system.schemas.schemas import Student as StudentSchema

from api.students.repositories.student_repository import StudentRepository

from api.students.errors.student_already_exists import StudentAlreadyExists


class CreateStudentUseCase:
    def __init__(self, student_repository: StudentRepository):
        self.student_repository = student_repository

    def execute(self, request: StudentCreate, current_user: Tuple[str, bool]) -> StudentSchema:
        _, is_admin = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        if self.student_repository.find_by_reg_no(request.reg_no):
            raise StudentAlreadyExists("Student already exists")

        student = Student(
            reg_no=request.reg_no,
            student_name=request.student_name,
            personal_circumstances=request.personal_circumstances,
        )

        self.student_repository.add(student)

        return student
