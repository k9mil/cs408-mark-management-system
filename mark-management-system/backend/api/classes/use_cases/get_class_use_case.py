from typing import Tuple

from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.class_not_found import ClassNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassUseCase:
    """
    The Use Case containing business logic for retrieving a particular class.
    """
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository) -> None:
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, class_code: str, current_user: Tuple[str, bool, bool]) -> ClassSchema:
        """
        Executes the Use Case for retrieving a particular class.

        Args:
            class_code: The `class_code` of the class.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user (from the JWT) cannot be found.
            PermissionError: If the requestor is not a user & a lecturer, or an administrator. Also if it's not the lecturer of the class provided.
        
        Returns:
            ClassSchema: A ClassSchema object containing all information about the requested class.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)
        
        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        class_ = self.class_repository.find_by_code(class_code)

        if class_ is None:
            raise ClassNotFound("Class not found")
        
        if class_.lecturer_id != user.id:
            raise PermissionError("Permission denied to access this resource")

        return class_
