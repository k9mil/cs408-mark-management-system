from fastapi import Depends

from api.middleware.dependencies import AcademicMisconductRepository
from api.middleware.dependencies import UserRepository
from api.middleware.dependencies import StudentRepository
from api.middleware.dependencies import ClassRepository

from api.academic_misconducts.use_cases.create_academic_misconduct_use_case import CreateAcademicMisconductUseCase
from api.academic_misconducts.use_cases.get_academic_misconducts_for_student_use_case import GetAcademicMisconductsForStudentUseCase

from api.middleware.dependencies import get_academic_misconduct_repository
from api.middleware.dependencies import get_user_repository
from api.middleware.dependencies import get_student_repository
from api.middleware.dependencies import get_class_repository


def create_academic_misconduct_use_case(
        academic_misconduct_repository: AcademicMisconductRepository = Depends(get_academic_misconduct_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        student_repository: StudentRepository = Depends(get_student_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> CreateAcademicMisconductUseCase:
    return CreateAcademicMisconductUseCase(
        academic_misconduct_repository, 
        user_repository,
        student_repository,
        class_repository
    )

def get_academic_misconducts_for_student_use_case(
        academic_misconduct_repository: AcademicMisconductRepository = Depends(get_academic_misconduct_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        student_repository: StudentRepository = Depends(get_student_repository),
    ) -> GetAcademicMisconductsForStudentUseCase:
    return GetAcademicMisconductsForStudentUseCase(
        academic_misconduct_repository, 
        user_repository,
        student_repository
    )
