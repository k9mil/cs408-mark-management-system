from fastapi import Depends

from api.middleware.dependencies import PersonalCircumstanceRepository
from api.middleware.dependencies import UserRepository

from api.personal_circumstances.use_cases.create_personal_circumstance_use_case import CreatePersonalCircumstanceUseCase
from api.personal_circumstances.use_cases.get_personal_circumstances_for_student_use_case import GetPersonalCircumstancesForStudentUseCase

from api.middleware.dependencies import get_personal_circumstance_repository
from api.middleware.dependencies import get_user_repository


def create_personal_circumstance_use_case(
        personal_circumstance_repository: PersonalCircumstanceRepository = Depends(get_personal_circumstance_repository),
    ) -> CreatePersonalCircumstanceUseCase:
    return CreatePersonalCircumstanceUseCase(
        personal_circumstance_repository, 
    )

def get_personal_circumstances_for_student_use_case(
        personal_circumstance_repository: PersonalCircumstanceRepository = Depends(get_personal_circumstance_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetPersonalCircumstancesForStudentUseCase:
    return GetPersonalCircumstancesForStudentUseCase(
        personal_circumstance_repository, 
        user_repository, 
    )
