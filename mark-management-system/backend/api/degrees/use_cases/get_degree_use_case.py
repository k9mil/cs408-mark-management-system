from typing import Tuple

from api.system.schemas.schemas import Degree as DegreeSchema

from api.degrees.repositories.degree_repository import DegreeRepository
from api.users.repositories.user_repository import UserRepository

from api.degrees.errors.degree_not_found import DegreeNotFound


class GetDegreeUseCase:
    def __init__(self, degree_repository: DegreeRepository, user_repository: UserRepository):
        self.degree_repository = degree_repository
        self.user_repository = user_repository
    
    def execute(self, degree_name: str, current_user: Tuple[str, bool]) -> DegreeSchema:
        user_email, is_admin = current_user

        lecturer = self.user_repository.find_by_email(user_email)

        if lecturer is None and is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        degree = self.degree_repository.find_by_name(degree_name)

        if degree is None:
            raise DegreeNotFound("Degree not found")

        return degree
