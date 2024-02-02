from fastapi import Depends

from api.middleware.dependencies import DegreeRepository
from api.middleware.dependencies import UserRepository

from api.degrees.use_cases.create_degree_use_case import CreateDegreeUseCase
from api.degrees.use_cases.get_degree_use_case import GetDegreeUseCase
from api.degrees.use_cases.get_degrees_use_case import GetDegreesUseCase

from api.middleware.dependencies import get_degree_repository
from api.middleware.dependencies import get_user_repository


def create_degree_use_case(
        degree_repository: DegreeRepository = Depends(get_degree_repository),
    ) -> CreateDegreeUseCase:
    return CreateDegreeUseCase(
        degree_repository, 
    )

def get_degree_use_case(
        degree_repository: DegreeRepository = Depends(get_degree_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetDegreeUseCase:
    return GetDegreeUseCase(
        degree_repository,
        user_repository
    )

def get_degrees_use_case(
        degree_repository: DegreeRepository = Depends(get_degree_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetDegreesUseCase:
    return GetDegreesUseCase(
        degree_repository,
        user_repository
    )
