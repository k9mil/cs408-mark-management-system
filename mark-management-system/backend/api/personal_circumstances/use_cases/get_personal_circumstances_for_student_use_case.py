from typing import Tuple, List

from api.system.schemas.schemas import PersonalCircumstancesBase as PersonalCircumstanceSchema

from api.personal_circumstances.repositories.personal_circumstance_repostitory import PersonalCircumstanceRepository
from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_not_found import UserNotFound

from api.personal_circumstances.errors.personal_circumstances_not_found import PersonalCircumstanceNotFound

class GetPersonalCircumstancesForStudentUseCase:
    """
    The Use Case containing business logic for retrieving all personal circumstances for a student.
    """
    def __init__(self, personal_circumstance_repository: PersonalCircumstanceRepository, user_repository: UserRepository) -> None:
        self.personal_circumstance_repository = personal_circumstance_repository
        self.user_repository = user_repository

    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> List[PersonalCircumstanceSchema]:
        """
        Executes the Use Case to retrieve all personal circumstances for a particular student in the system.

        Args:
            reg_no: The stuuent for which to retrieve the data.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user from the JWT token is not found.
            PermissionError: If the user is not valid and a lecturer, or if they are not an aministrator.
            PersonalCircumstanceNotFound: If no personal circumstances are found.
        
        Returns:
            List[PersonalCircumstanceSchema]: A list of PersonalCircumstancesBase schema object containing key information about the personal circumstances.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        personal_circumstances = self.personal_circumstance_repository.get_by_student_reg_no(reg_no)

        if personal_circumstances is None:
            raise PersonalCircumstanceNotFound("No personal circumstances found")
        
        return personal_circumstances
