from typing import Tuple

from api.classes.repositories.class_repository import ClassRepository

from api.classes.errors.class_not_found import ClassNotFound


class DeleteClassUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.class_repository = class_repository
    
    def execute(self, class_id: int, current_user: Tuple[str, bool]) -> None:
        _, is_admin = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        class_ = self.class_repository.get_class(class_id)

        if class_ is None:
            raise ClassNotFound("Class not found")

        self.class_repository.delete(class_)
