from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository

from api.classes.errors.classes_not_found import ClassesNotFound


class GetClassesUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.class_repository = class_repository
    
    def execute(self, skip: int, limit: int) -> list[ClassSchema]:
        print("test")
        
        classes = self.class_repository.get_classes(skip, limit)

        if classes is None:
            raise ClassesNotFound("Classes not found")

        return classes
