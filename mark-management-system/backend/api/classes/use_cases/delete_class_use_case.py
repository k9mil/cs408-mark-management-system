from api.classes.repositories.class_repository import ClassRepository

from api.classes.errors.class_not_found import ClassNotFound


class DeleteClassUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.class_repository = class_repository
    
    def execute(self, class_id: int) -> None:
        class_ = self.class_repository.get_class(class_id)

        if class_ is None:
            raise ClassNotFound("Class not found")

        self.class_repository.delete(class_)
