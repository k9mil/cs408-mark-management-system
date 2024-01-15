from api.system.models.models import Class

from api.system.schemas.schemas import ClassCreate
from api.system.schemas.schemas import Class as ClassSchema

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.errors.class_already_exists import ClassAlreadyExists
from api.users.errors.user_not_found import UserNotFound


class CreateClassUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository

    def execute(self, request: ClassCreate) -> ClassSchema:
        if self.class_repository.find_by_code(request.code):
            raise ClassAlreadyExists("Class already exists")
        
        lecturer = self.user_repository.get_user(request.lecturer_id)

        if lecturer is None:
            raise UserNotFound("Lecturer not found")
        
        class_ = Class(
            name=request.name,
            code=request.code,
            credit=request.credit,
            credit_level=request.credit_level,
            lecturer=lecturer,
        )

        self.class_repository.add(class_)

        return class_
