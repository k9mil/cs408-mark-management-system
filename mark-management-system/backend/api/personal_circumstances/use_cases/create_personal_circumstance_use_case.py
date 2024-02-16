from typing import Tuple

from api.system.models.models import PersonalCircumstance

from api.system.schemas.schemas import PersonalCircumstancesBase as PersonalCircumstanceSchema
from api.system.schemas.schemas import PersonalCircumstancesCreate

from api.personal_circumstances.repositories.personal_circumstance_repostitory import PersonalCircumstanceRepository

from api.personal_circumstances.errors.personal_circumstances_already_exist import PersonalCircumstanceAlreadyExists


class CreatePersonalCircumstanceUseCase:
    """
    The Use Case containing business logic for creating a new personal circumstance.
    """
    def __init__(self, personal_circumstance_repository: PersonalCircumstanceRepository) -> None:
        self.personal_circumstance_repository = personal_circumstance_repository

    def execute(self, request: PersonalCircumstancesCreate, current_user: Tuple[str, bool, bool]) -> PersonalCircumstanceSchema:
        """
        Executes the Use Case to create a new personal circumstance in the system.

        Args:
            request: A `DegreeCreate` object is required which contains the necessary degree details for degree creation.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an administrator.
            PersonalCircumstanceAlreadyExists: If the personal circumstance already exists.
        
        Returns:
            PersonalCircumstanceSchema: A PersonalCircumstanceBase schema object containing all information about the newly created personal circumstances.
        """
        # _, is_admin, _ = current_user

        # if is_admin is False:
        #     raise PermissionError("Permission denied to access this resource")
        
        if self.personal_circumstance_repository.find_by_details(request):
            raise PersonalCircumstanceAlreadyExists("Personal Circumstance already exists")

        personal_circumstance = PersonalCircumstance(
            details=request.details,
            semester=request.semester,
            cat=request.cat,
            comments=request.comments,
            student_reg_no=request.reg_no
        )

        self.personal_circumstance_repository.add(personal_circumstance)
        
        return personal_circumstance
