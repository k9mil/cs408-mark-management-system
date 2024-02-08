from typing import Tuple

from api.system.models.models import Class

from api.system.schemas.schemas import Class as ClassSchema
from api.system.schemas.schemas import ClassCreate

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.class_already_exists import ClassAlreadyExists
from api.users.errors.user_not_found import UserNotFound


class CreateClassUseCase:
    """
    The Use Case containing business logic for creating a new class.
    """
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository) -> None:
        self.class_repository = class_repository
        self.user_repository = user_repository

    def execute(self, request: ClassCreate, current_user: Tuple[str, bool, bool]) -> ClassSchema:
        """
        Executes the Use Case to create a new class in the system.

        Args:
            request: A `ClassCreate` object is required which contains the necessary class details for class creation.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an administrator.
            ClassAlreadyExists: If the class already exists.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            ClassSchema: A ClassSchema schema object containing all information about the newly created class.
        """
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        if self.class_repository.find_by_code(request.code):
            raise ClassAlreadyExists("Class already exists")
        
        lecturer = self.user_repository.find_by_id(request.lecturer_id)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")

        class_ = Class(
            name=request.name,
            code=request.code,
            credit=request.credit,
            credit_level=request.credit_level,
            lecturer=lecturer,
        )

        self.class_repository.add(class_)

        return class_
