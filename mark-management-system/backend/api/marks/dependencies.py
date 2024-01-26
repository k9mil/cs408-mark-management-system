from fastapi import Depends

from api.middleware.dependencies import MarkRepository
from api.middleware.dependencies import UserRepository

from api.marks.use_cases.create_mark_use_case import CreateMarkUseCase
from api.marks.use_cases.get_mark_use_case import GetMarkUseCase
from api.marks.use_cases.get_student_marks_use_case import GetStudentMarksUseCase
from api.marks.use_cases.delete_mark_use_case import DeleteMarkUseCase

from api.middleware.dependencies import get_mark_repository
from api.middleware.dependencies import get_user_repository


def create_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
    ) -> CreateMarkUseCase:
    return CreateMarkUseCase(
        mark_repository, 
    )

def get_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetMarkUseCase:
    return GetMarkUseCase(
        mark_repository,
        user_repository
    )

def get_student_marks_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetStudentMarksUseCase:
    return GetStudentMarksUseCase(
        mark_repository,
        user_repository
    )

def delete_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
    ) -> DeleteMarkUseCase:
    return DeleteMarkUseCase(
        mark_repository,
    )
