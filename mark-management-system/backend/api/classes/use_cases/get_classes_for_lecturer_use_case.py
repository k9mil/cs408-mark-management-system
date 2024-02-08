from typing import Tuple, List

from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.classes_not_found import ClassesNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassesForLecturerUseCase:
    """
    The Use Case containing business logic for retrieving a list of classes for a particular lecturer.
    """
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository) -> None:
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, current_user: Tuple[str, bool, bool], skip: int, limit: int) -> List[ClassSchema]:
        """
        Executes the Use Case for retrieving a list of classes for a particular lecturer.

        Args:
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.
            skip: The amount to skip.
            limit: The maximum number of items to be retrieved.

        Raises:
            UserNotFound: If the user (from the JWT) cannot be found.
            ClassesNotFound: If no classes are returned from the repository.

        Returns:
            List[ClassSchema]: A list of `ClassSchema` objects, containing the information about the classes.
        """
        user_email, _, _ = current_user

        lecturer = self.user_repository.find_by_email(user_email)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")

        classes = self.class_repository.get_classes_by_lecturer_id(lecturer.id, skip, limit)

        if classes is None:
            raise ClassesNotFound("Classes not found")

        return classes
