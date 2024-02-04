from typing import Tuple

from api.system.schemas.schemas import ClassBase

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository
from api.degrees.repositories.degree_repository import DegreeRepository

from api.classes.errors.class_not_found import ClassNotFound
from api.classes.errors.class_not_associated_with_degree import ClassNotAssociatedWithDegree

from api.users.errors.user_not_found import UserNotFound

from api.degrees.errors.degree_not_found import DegreeNotFound


class CheckIfClassIsAssociatedWithADegreeUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository, degree_repository: DegreeRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository
        self.degree_repository = degree_repository
    
    def execute(
            self,
            class_code: str,
            degree_name: str,
            degree_level: str,
            current_user: Tuple[str, bool, bool]
        ) -> ClassBase:
        user_email, _, _ = current_user

        lecturer = self.user_repository.find_by_email(user_email)
        
        if lecturer is None:
            raise UserNotFound("User not found")
        
        class_ = self.class_repository.find_by_code(class_code)

        if class_ is None:
            raise ClassNotFound("Class not found")
        
        degree = self.degree_repository.find_by_name_and_level(degree_name, degree_level)
        
        if degree is None:
            raise DegreeNotFound("Degree not found")
        
        class_associated_with_degree = self.degree_repository.is_class_associated_with_degree(
            degree.id,
            class_.id,
        )

        if class_associated_with_degree is None:
            raise ClassNotAssociatedWithDegree("Class does not belong to the provided degree")
        
        return class_
