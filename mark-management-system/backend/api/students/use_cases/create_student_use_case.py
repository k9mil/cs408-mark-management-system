from typing import Tuple

from api.system.models.models import Student

from api.system.schemas.schemas import StudentCreate
from api.system.schemas.schemas import Student as StudentSchema

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.students.errors.student_already_exists import StudentAlreadyExists

from api.users.errors.user_not_found import UserNotFound


class CreateStudentUseCase:
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository

    def execute(self, request: StudentCreate, current_user: Tuple[str, bool, bool]) -> StudentSchema:
        user_email, is_admin, is_lecturer = current_user

        # TODO: temporarily lecturers can create students, i.e. when they upload marks.

        user = self.user_repository.find_by_email(user_email)
        
        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        if self.student_repository.find_by_reg_no(request.reg_no):
            raise StudentAlreadyExists("Student already exists")

        if request.personal_circumstances:
            student = Student(
                reg_no=request.reg_no,
                student_name=request.student_name,
                personal_circumstances=request.personal_circumstances,
                degree_id=request.degree_id,
            )
        else:
           student = Student(
                reg_no=request.reg_no,
                student_name=request.student_name,
                degree_id=request.degree_id,
            )

        self.student_repository.add(student)

        return student
