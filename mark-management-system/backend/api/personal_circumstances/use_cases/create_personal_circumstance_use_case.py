from typing import Tuple

from api.system.models.models import PersonalCircumstance

from api.system.schemas.schemas import PersonalCircumstancesBase as PersonalCircumstanceSchema
from api.system.schemas.schemas import PersonalCircumstancesCreate

from api.personal_circumstances.repositories.personal_circumstance_repostitory import PersonalCircumstanceRepository
from api.users.repositories.user_repository import UserRepository
from api.students.repositories.student_repository import StudentRepository

from api.personal_circumstances.errors.personal_circumstances_already_exist import PersonalCircumstanceAlreadyExists

from api.users.errors.user_not_found import UserNotFound

from api.students.errors.student_not_found import StudentNotFound

class CreatePersonalCircumstanceUseCase:
    """
    The Use Case containing business logic for creating a new personal circumstance.
    """
    def __init__(
            self,
            personal_circumstance_repository: PersonalCircumstanceRepository,
            user_repository: UserRepository,
            student_repository: StudentRepository
        ) -> None:
        self.personal_circumstance_repository = personal_circumstance_repository
        self.user_repository = user_repository
        self.student_repository = student_repository

    def execute(self, request: PersonalCircumstancesCreate, current_user: Tuple[str, bool, bool]) -> PersonalCircumstanceSchema:
        """
        Executes the Use Case to create a new personal circumstance in the system.

        Args:
            request: A `PersonalCircumstancesCreate` object is required which contains the necessary degree details for personal circumstance creation.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user from the JWT token is not found.
            PermissionError: If the user is not valid and a lecturer, or if they are not an administrator.
            StudentNotFound: If the student from the request is not found.
            PersonalCircumstanceAlreadyExists: If the personal circumstance already exists.
        
        Returns:
            PersonalCircumstanceSchema: A PersonalCircumstanceBase schema object containing all information about the newly created personal circumstances.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        if self.student_repository.find_by_reg_no(request.reg_no) is None:
            raise StudentNotFound("Student not found")
        
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
