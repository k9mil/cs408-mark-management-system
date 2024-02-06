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
    """
    The Use Case containing business logic for checking whether a class is associated with a particular degree.
    """
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository, degree_repository: DegreeRepository) -> None:
        self.class_repository = class_repository
        self.user_repository = user_repository
        self.degree_repository = degree_repository
    
    def execute(
            self,
            class_code: str,
            degree_level: str,
            degree_name: str,
            current_user: Tuple[str, bool, bool]
        ) -> ClassBase:
        """
        Executes the Use Case to check if a class is associated with a specific degree.

        Args:
            class_code: The `class_code` of the class which is to be checked.
            degree_level: The `degree_level` of the degree which is to be checked against.
            degree_name: The `degree_name` of the degree which is to be checked against.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user (from the JWT) cannot be found.
            ClassNotFound: If the class is not found, given the class_code passed in.
            DegreeNotFound: If the degree is not found, given the name and level passed in.
            ClassNotAssociatedWithDegree: If the class is not associated with the degree.

        Returns:
            ClassBase: A ClassBase schema object containing the name, code, credit and credit level of the class.
        """
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
            raise ClassNotAssociatedWithDegree(f"Class {class_code} does not belong to the {degree_level} {degree_name} degree")
        
        return class_
