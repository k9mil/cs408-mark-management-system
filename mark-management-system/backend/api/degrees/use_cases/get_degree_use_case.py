from typing import Tuple

from api.system.schemas.schemas import Degree as DegreeSchema

from api.degrees.repositories.degree_repository import DegreeRepository
from api.users.repositories.user_repository import UserRepository

from api.degrees.errors.degree_not_found import DegreeNotFound

from api.users.errors.user_not_found import UserNotFound

class GetDegreeUseCase:
    def __init__(self, degree_repository: DegreeRepository, user_repository: UserRepository):
        self.degree_repository = degree_repository
        self.user_repository = user_repository
    
    def execute(self, degree_name: str, current_user: Tuple[str, bool, bool]) -> DegreeSchema:
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
