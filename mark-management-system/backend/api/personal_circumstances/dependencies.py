from fastapi import Depends

from api.middleware.dependencies import PersonalCircumstanceRepository

from api.personal_circumstances.use_cases.create_personal_circumstance_use_case import CreatePersonalCircumstanceUseCase

from api.middleware.dependencies import get_personal_circumstance_repository

def create_personal_circumstance_use_case(
        personal_circumstance_repository: PersonalCircumstanceRepository = Depends(get_personal_circumstance_repository),
    ) -> CreatePersonalCircumstanceUseCase:
    return CreatePersonalCircumstanceUseCase(
        personal_circumstance_repository, 
    )
