from typing import Tuple

from api.system.models.models import Degree

from api.system.schemas.schemas import DegreeCreate
from api.system.schemas.schemas import Degree as DegreeSchema

from api.degrees.repositories.degree_repository import DegreeRepository

from api.degrees.errors.degree_already_exists import DegreeAlreadyExists


class CreateDegreeUseCase:
    def __init__(self, degree_repository: DegreeRepository):
        self.degree_repository = degree_repository

    def execute(self, request: DegreeCreate, current_user: Tuple[str, bool]) -> DegreeSchema:
        _, is_admin = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        if self.degree_repository.find_by_name(request.name):
            raise DegreeAlreadyExists("Degree already exists")

        degree = Degree(
            level=request.level,
            name=request.name,
        )

        self.degree_repository.add(degree)

        return degree
