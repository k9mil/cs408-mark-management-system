from typing import Tuple

from api.system.schemas.schemas import Class as ClassSchema
from api.system.schemas.schemas import ClassEdit

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.class_not_found import ClassNotFound
from api.classes.errors.class_already_exists import ClassAlreadyExists

from api.users.errors.user_not_found import UserNotFound


class EditClassUseCase:
    """
    The Use Case containing business logic for editing an existing class.
    """
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository) -> None:
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, request: ClassEdit, current_user: Tuple[str, bool, bool]) -> ClassSchema:      
        """
        Executes the Use Case to edit an existing class in the system.

        Args:
            request: A `ClassEdit` object is which contains all of the new fields, as well as the original code & lecturer_id.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an administrator.
            ClassAlreadyExists: If the class already exists (i.e. the user is trying to modify the code of the class to be something that already exists).
            ClassNotFound: If the class_id in the request cannot be found.
            UserNotFound: If the lectuer in the request cannot be found.

        Returns:
            ClassSchema: A ClassSchema schema object containing all information about the newly edited class.
        """
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")

        if request.code != request.original_code:
            class_already_exists = self.class_repository.check_class_code_exists(request)

            if class_already_exists:
                raise ClassAlreadyExists("Class already exists")

        class_ = self.class_repository.get_class(request.id)

        if class_ is None:
            raise ClassNotFound("Class not found")
        
        lecturer = self.user_repository.find_by_id(request.lecturer_id)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")

        self.class_repository.update(class_, lecturer, request)

        return class_
