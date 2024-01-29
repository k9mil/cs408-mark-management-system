from typing import Tuple, List

from api.system.schemas.schemas import User as UserSchema

from api.users.repositories.user_repository import UserRepository

from api.users.errors.lecturers_not_found import LecturersNotFound


class GetLecturersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, skip: int, limit: int, current_user: Tuple[str, bool]) -> List[UserSchema]:
        _, is_admin = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        lecturers = self.user_repository.get_lecturers(skip, limit)

        if lecturers is None:
            raise LecturersNotFound("Users not found")

        return lecturers
