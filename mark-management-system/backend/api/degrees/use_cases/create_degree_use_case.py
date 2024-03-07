from typing import Tuple

from api.system.models.models import Degree

from api.system.schemas.schemas import Degree as DegreeSchema
from api.system.schemas.schemas import DegreeCreate

from api.degrees.repositories.degree_repository import DegreeRepository

from api.degrees.errors.degree_already_exists import DegreeAlreadyExists


class CreateDegreeUseCase:
    """
    The Use Case containing business logic for creating a new degree.
    """
    def __init__(self, degree_repository: DegreeRepository) -> None:
        self.degree_repository = degree_repository

    def execute(self, request: DegreeCreate, current_user: Tuple[str, bool, bool]) -> DegreeSchema:
        """
        Executes the Use Case to create a new degree in the system.

        Args:
            request: A `DegreeCreate` object is required which contains the necessary degree details for degree creation.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an administrator.
            DegreeAlreadyExists: If the degree already exists.
        
        Returns:
            DegreeSchema: A DegreeSchema schema object containing all information about the newly created degree.
        """
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        if self.degree_repository.find_by_name(request.name):
            raise DegreeAlreadyExists("Degree already exists")

        degree = Degree(
            level=request.level,
            name=request.name,
            code=request.code,
        )

        self.degree_repository.add(degree)

        return degree
