from fastapi import Depends

from api.middleware.dependencies import DegreeRepository

from api.degrees.use_cases.create_degree_use_case import CreateDegreeUseCase

from api.middleware.dependencies import get_degree_repository


def create_degree_use_case(
        get_degree_repository: DegreeRepository = Depends(get_degree_repository),
    ) -> CreateDegreeUseCase:
    return CreateDegreeUseCase(
        get_degree_repository, 
    )
