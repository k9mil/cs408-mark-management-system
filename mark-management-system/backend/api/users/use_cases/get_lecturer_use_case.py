from typing import Tuple, List

from api.system.schemas.schemas import Lecturer
from api.system.schemas.schemas import Class
from api.system.schemas.schemas import LecturerClass

from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository
from api.marks.repositories.mark_repository import MarkRepository

from api.users.errors.user_not_found import UserNotFound


class GetLecturerUseCase:
    def __init__(
            self, 
            user_repository: UserRepository,
            class_repository: ClassRepository,
            mark_repository: MarkRepository
        ):
        self.user_repository = user_repository
        self.class_repository = class_repository
        self.mark_repository = mark_repository
    
    def execute(self, user_id: int, current_user: Tuple[str, bool]) -> Lecturer:
        user_email, _ = current_user

        lecturer = self.user_repository.find_by_email(user_email)

        if lecturer is None:
            raise UserNotFound("User not found")
        
        classes = self.class_repository.get_classes_by_lecturer_id(lecturer.id)

        class_list: List = []

        for class_ in classes:
            class_list.append(self.create_lecturer_class(class_))

        lecturer_data = Lecturer(
            id=lecturer.id,
            first_name=lecturer.first_name,
            last_name=lecturer.last_name,
            number_of_classes_taught=len(classes),
            classes=class_list
        )

        return lecturer_data

    def create_lecturer_class(self, class_: Class) -> LecturerClass:
        marks = self.mark_repository.get_student_marks_for_class(class_.id)

        return LecturerClass(
            name=class_.name,
            code=class_.code,
            credit=class_.credit,
            credit_level=class_.credit_level,
            is_uploaded=len(marks) > 0,
        )
