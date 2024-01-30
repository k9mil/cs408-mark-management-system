from typing import Tuple, List

from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.classes_not_found import ClassesNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassesForLecturerUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository
    
    def execute(self, current_user: Tuple[str, bool], skip: int, limit: int) -> List[ClassSchema]:
        user_email, _ = current_user

        lecturer = self.user_repository.find_by_email(user_email)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")

        classes = self.class_repository.get_classes_by_lecturer_id(lecturer.id, skip, limit)

        if classes is None:
            raise ClassesNotFound("Classes not found")

        return classes
