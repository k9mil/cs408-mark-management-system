from api.system.schemas.schemas import Class as ClassSchema

from api.system.schemas.schemas import ClassEdit

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.class_not_found import ClassNotFound

from api.users.errors.user_not_found import UserNotFound


class EditClassUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, request: ClassEdit) -> ClassSchema:
        class_ = self.class_repository.get_class(request.id)

        if class_ is None:
            raise ClassNotFound("Class not found")
        
        lecturer = self.user_repository.get_user(request.lecturer_id)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")

        self.class_repository.update(class_, lecturer, request)

        return class_
