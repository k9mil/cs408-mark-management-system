from fastapi import Depends

from api.middleware.dependencies import StudentRepository

from api.students.use_cases.create_student_use_case import CreateStudentUseCase

from api.middleware.dependencies import get_student_repository


def create_student_use_case(
        student_repository: StudentRepository = Depends(get_student_repository),
    ) -> CreateStudentUseCase:
    return CreateStudentUseCase(
        student_repository, 
    )
