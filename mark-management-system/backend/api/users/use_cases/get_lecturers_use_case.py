from typing import Tuple, List

from api.system.schemas.schemas import Lecturer
from api.system.schemas.schemas import Class
from api.system.schemas.schemas import LecturerClass

from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository
from api.marks.repositories.mark_repository import MarkRepository

from api.users.errors.lecturers_not_found import LecturersNotFound


class GetLecturersUseCase:
    def __init__(
            self, 
            user_repository: UserRepository,
            class_repository: ClassRepository,
            mark_repository: MarkRepository
        ):
        self.user_repository = user_repository
        self.class_repository = class_repository
        self.mark_repository = mark_repository
    
    def execute(self, skip: int, limit: int, current_user: Tuple[str, bool, bool]) -> List[Lecturer]:
        _, is_admin, _ = current_user

        if is_admin is False:
            raise PermissionError("Permission denied to access this resource")
        
        lecturers = self.user_repository.get_lecturers(skip, limit)

        if lecturers is None:
            raise LecturersNotFound("Users not found")
        
        lecturers_with_classes: List = []

        for lecturer in lecturers:
            classes = self.class_repository.get_classes_by_lecturer_id(lecturer.id, skip, limit)

            class_list: List = [self.create_lecturer_class(class_) for class_ in classes]

            lecturer_data = Lecturer(
                id=lecturer.id,
                first_name=lecturer.first_name,
                last_name=lecturer.last_name,
                number_of_classes_taught=len(classes),
                classes=class_list
            )

            lecturers_with_classes.append(lecturer_data)


        return lecturers_with_classes

    def create_lecturer_class(self, class_: Class) -> LecturerClass:
        marks = self.mark_repository.get_student_marks_for_class(class_.id)

        return LecturerClass(
            name=class_.name,
            code=class_.code,
            credit=class_.credit,
            credit_level=class_.credit_level,
            is_uploaded=len(marks) > 0,
        )
