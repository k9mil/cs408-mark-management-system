from typing import Tuple, List

from api.system.schemas.schemas import Lecturer
from api.system.schemas.schemas import Class
from api.system.schemas.schemas import LecturerClass

from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository
from api.marks.repositories.mark_repository import MarkRepository

from api.users.errors.user_not_found import UserNotFound


class GetLecturerUseCase:
    """
    The Use Case containing business logic for retrieving a lecturer's details.

    Note: No identifier is passed in, only the requestor can view the lecturer (their own) details, via JWT.
    """
    def __init__(
            self, 
            user_repository: UserRepository,
            class_repository: ClassRepository,
            mark_repository: MarkRepository
        ) -> None:
        self.user_repository = user_repository
        self.class_repository = class_repository
        self.mark_repository = mark_repository
    
    def execute(self, current_user: Tuple[str, bool, bool]) -> Lecturer:
        """
        Executes the Use Case to retrieve a lecturer's details.

        Since a Lecturer schema contains also various other details, such as number of classes taught & classes they teach, that data
        is calculated in this use case.

        Args:
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user is not found.

        Returns:
            Lecturer: A Lecturer schema object containing the lecturer details.
        """
        user_email, _, _ = current_user

        lecturer = self.user_repository.find_by_email(user_email)

        if lecturer is None:
            raise UserNotFound("User not found")
        
        classes = self.class_repository.get_classes_by_lecturer_id(lecturer.id)

        class_list: List = [self.create_lecturer_class(class_) for class_ in classes]

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
