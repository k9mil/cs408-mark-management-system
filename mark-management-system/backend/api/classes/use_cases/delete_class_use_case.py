from typing import Tuple

from api.classes.repositories.class_repository import ClassRepository

from api.classes.errors.class_not_found import ClassNotFound


class DeleteClassUseCase:
    """
    The Use Case containing business logic for deleting an existing class.
    """
    def __init__(self, class_repository: ClassRepository) -> None:
        self.class_repository = class_repository
    
    def execute(self, class_id: int, current_user: Tuple[str, bool, bool]) -> None:
        """
        Executes the Use Case to create a new class in the system.

        Args:
            class_id: The identifier of the class to be deleted.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not an administrator.
            ClassNotFound: If the class cannot be found.
        """
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        class_ = self.class_repository.get_class(class_id)

        if class_ is None:
            raise ClassNotFound("Class not found")

        self.class_repository.delete(class_)
