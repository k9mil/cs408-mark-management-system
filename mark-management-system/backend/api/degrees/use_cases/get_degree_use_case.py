from typing import Tuple

from api.system.schemas.schemas import Degree as DegreeSchema

from api.degrees.repositories.degree_repository import DegreeRepository
from api.users.repositories.user_repository import UserRepository

from api.degrees.errors.degree_not_found import DegreeNotFound

from api.users.errors.user_not_found import UserNotFound

class GetDegreeUseCase:
    """
    The Use Case containing business logic for retrieving a particular degree.
    """
    def __init__(self, degree_repository: DegreeRepository, user_repository: UserRepository) -> None:
        self.degree_repository = degree_repository
        self.user_repository = user_repository
    
    def execute(self, degree_name: str, current_user: Tuple[str, bool, bool]) -> DegreeSchema:
        """
        Executes the Use Case to retrieve a particular degree.

        Args:
            degree_name: The degree name which will be used for querying the degree.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user (from the JWT) is not found.
            PermissionError: If the requestor is not either a user & a lecturer, or an administrator.
            DegreeNotFound: If the degree is not found.
        
        Returns:
            DegreeSchema: A DegreeSchema schema object containing all information about the degree.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        degree = self.degree_repository.find_by_name(degree_name)

        if degree is None:
            raise DegreeNotFound("Degree not found")

        return degree
