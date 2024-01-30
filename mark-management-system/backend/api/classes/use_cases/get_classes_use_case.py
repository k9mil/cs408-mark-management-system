from typing import Tuple, List

from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository

from api.classes.errors.classes_not_found import ClassesNotFound


class GetClassesUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.class_repository = class_repository
    
    def execute(self, skip: int, limit: int, current_user: Tuple[str, bool]) -> List[ClassSchema]:
        _, is_admin = current_user
        
        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        classes = self.class_repository.get_classes(skip, limit)

        if classes is None:
            raise ClassesNotFound("Classes not found")

        return classes
