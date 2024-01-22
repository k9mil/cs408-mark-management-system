from fastapi import Depends

from api.middleware.dependencies import MarkRepository

from api.marks.use_cases.create_mark_use_case import CreateMarkUseCase

from api.middleware.dependencies import get_mark_repository


def create_mark_use_case(
        mark_repository: MarkRepository = Depends(get_mark_repository),
    ) -> CreateMarkUseCase:
    return CreateMarkUseCase(
        mark_repository, 
    )
