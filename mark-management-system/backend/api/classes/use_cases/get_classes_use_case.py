from typing import Tuple, List

from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository

from api.classes.errors.classes_not_found import ClassesNotFound


class GetClassesUseCase:
    """
    The Use Case containing business logic for retrieving a list of classes.
    """
    def __init__(self, class_repository: ClassRepository) -> None:
        self.class_repository = class_repository
    
    def execute(self, skip: int, limit: int, current_user: Tuple[str, bool, bool]) -> List[ClassSchema]:
        """
        Executes the Use Case for retrieving a list of classes.

        Args:
            skip: The amount to skip.
            limit: The maximum number of items to be retrieved.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.
        
        Raises:
            PermissionError: If the requestor is not an administrator.
            ClassesNotFound: If no classes are returned from the repository.

        Returns:
            List[ClassSchema]: A list of `ClassSchema` objects, containing hte information about the classes.
        """
        _, is_admin, _ = current_user
        
        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        classes = self.class_repository.get_classes(skip, limit)

        if classes is None:
            raise ClassesNotFound("Classes not found")

        return classes
