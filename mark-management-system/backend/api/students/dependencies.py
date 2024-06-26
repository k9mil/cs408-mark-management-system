from fastapi import Depends

from api.middleware.dependencies import StudentRepository
from api.middleware.dependencies import UserRepository
from api.middleware.dependencies import ClassRepository

from api.students.use_cases.create_student_use_case import CreateStudentUseCase
from api.students.use_cases.get_student_use_case import GetStudentUseCase
from api.students.use_cases.get_students_use_case import GetStudentsUseCase
from api.students.use_cases.get_student_statistics_use_case import GetStudentStatisticsUseCase

from api.middleware.dependencies import get_student_repository
from api.middleware.dependencies import get_user_repository
from api.middleware.dependencies import get_class_repository


def create_student_use_case(
        student_repository: StudentRepository = Depends(get_student_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> CreateStudentUseCase:
    return CreateStudentUseCase(
        student_repository,
        user_repository
    )

def get_student_use_case(
        student_repository: StudentRepository = Depends(get_student_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> GetStudentUseCase:
    return GetStudentUseCase(
        student_repository,
        user_repository, 
        class_repository
    )

def get_students_use_case(
        student_repository: StudentRepository = Depends(get_student_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetStudentsUseCase:
    return GetStudentsUseCase(
        student_repository,
        user_repository, 
    )

def get_student_statistics_use_case(
        student_repository: StudentRepository = Depends(get_student_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetStudentStatisticsUseCase:
    return GetStudentStatisticsUseCase(
        student_repository,
        user_repository, 
    )
