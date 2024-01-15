from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.classes_not_found import ClassesNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassesForLecturerUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, lecturer_id: int, skip: int, limit: int) -> list[ClassSchema]:
        lecturer = self.user_repository.get_user(lecturer_id)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")

        classes = self.class_repository.get_classes_by_lecturer_id(lecturer_id, skip, limit)

        if classes is None:
            raise ClassesNotFound("Classes not found")

        return classes
