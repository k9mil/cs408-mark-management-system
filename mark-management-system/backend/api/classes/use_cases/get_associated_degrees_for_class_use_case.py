from typing import Tuple, List

from api.system.schemas.schemas import DegreeBase

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository
from api.degrees.repositories.degree_repository import DegreeRepository

from api.classes.errors.class_not_found import ClassNotFound

from api.users.errors.user_not_found import UserNotFound

from api.degrees.errors.degrees_not_found import DegreesNotFound


class GetAssociatedDegreesForClassUseCase:
    """
    The Use Case containing business logic for retrieving associated degrees for a particular class.
    """
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository, degree_repository: DegreeRepository) -> None:
        self.class_repository = class_repository
        self.user_repository = user_repository
        self.degree_repository = degree_repository

    def execute(self, class_code: str, current_user: Tuple[str, bool, bool]) -> List[DegreeBase]:
        """
        Executes the Use Case to retrieve associated degrees for a particular class.

        Args:
            class_code: The `class_code` of the class.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the lecturer from the JWT cannot be found.
            ClassNotFound: If the class cannot be found via the class_code.
            DegreesNotFound: If a class code is found, but it has no associated degrees.

        Returns:
            List[DegreeBase]: A list of DegreeBase objects, containing a level & a name, i.e. all associated degrees with the class_code provided.
        """
        user_email, _, _ = current_user

        lecturer = self.user_repository.find_by_email(user_email)

        if lecturer is None:
            raise UserNotFound("User not found")

        class_ = self.class_repository.find_by_code(class_code)

        if class_ is None:
            raise ClassNotFound("Class not found")

        if len(class_.degrees) == 0:
            raise DegreesNotFound("Degrees not found")

        degrees: List = []

        for class_degree in class_.degrees:
            degree = DegreeBase(
                level=class_degree.level,
                name=class_degree.name
            )

            degrees.append(degree)

        return degrees
