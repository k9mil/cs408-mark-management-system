from fastapi import Depends

from api.middleware.dependencies import MarkRepository
from api.middleware.dependencies import UserRepository
from api.middleware.dependencies import ClassRepository
from api.middleware.dependencies import StudentRepository

from api.marks.use_cases.create_mark_use_case import CreateMarkUseCase
from api.marks.use_cases.get_mark_use_case import GetMarkUseCase
from api.marks.use_cases.get_student_marks_use_case import GetStudentMarksUseCase
from api.marks.use_cases.get_student_statistics_use_case import GetStudentStatisticsUseCase
from api.marks.use_cases.edit_mark_use_case import EditMarkUseCase
from api.marks.use_cases.delete_mark_use_case import DeleteMarkUseCase
from api.marks.use_cases.get_marks_for_student_use_case import GetMarksForStudentUseCase
from api.marks.use_cases.get_marks_for_class_use_case import GetMarksForClassUseCase

from api.middleware.dependencies import get_mark_repository
from api.middleware.dependencies import get_user_repository
from api.middleware.dependencies import get_class_repository
from api.middleware.dependencies import get_student_repository


def create_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> CreateMarkUseCase:
    return CreateMarkUseCase(
        mark_repository, 
        user_repository,
        class_repository
    )

def get_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> GetMarkUseCase:
    return GetMarkUseCase(
        mark_repository,
        user_repository,
        class_repository
    )

def get_student_marks_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetStudentMarksUseCase:
    return GetStudentMarksUseCase(
        mark_repository,
        user_repository
    )

def get_student_statistics_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetStudentStatisticsUseCase:
    return GetStudentStatisticsUseCase(
        mark_repository,
        user_repository
    )

def edit_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> EditMarkUseCase:
    return EditMarkUseCase(
        mark_repository,
        user_repository,
        class_repository
    )

def delete_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> DeleteMarkUseCase:
    return DeleteMarkUseCase(
        mark_repository,
        user_repository,
        class_repository
    )

def get_marks_for_student_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        student_repository: StudentRepository = Depends(get_student_repository),
        user_repository: UserRepository = Depends(get_user_repository),
    ) -> GetMarksForStudentUseCase:
    return GetMarksForStudentUseCase(
        mark_repository,
        student_repository,
        user_repository,
    )

def get_marks_for_class_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository),
    ) -> GetMarksForClassUseCase:
    return GetMarksForClassUseCase(
        mark_repository,
        user_repository,
    )
