from statistics import mean, mode, median

from typing import Tuple

from api.system.schemas.schemas import MarksStatistics

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassStatisticsUseCase:
    """
    The Use Case containing business logic for retrieving class data & calculating
    statistics for that class.
    """
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository) -> None:
        self.class_repository = class_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, class_code: str, current_user: Tuple[str, bool, bool]) -> MarksStatistics:
        """
        Executes the Use Case to calculate statistics of a given class.

        Args:
            class_code: The class code to which the metrics should be calculated for
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user (from the JWT) cannot be found.
            MarkNotFound: If no marks are found in the system.
        
        Returns:
            MarksStatistics: A MarksStatistics schema object containing statistics about the class, i.e. mean, mode median and pass rate
            as well as storing five performance buckets of students.
        """
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marks = self.class_repository.get_marks_for_class(class_code)

        if not marks:
            raise MarkNotFound("No marks found for the class")

        mark_data = []

        for current_mark in marks:
            if current_mark[1]:
                mark_data.append(current_mark[1])

        if mark_data:
            marks_statistics = MarksStatistics(
                mean=round(mean(mark_data)),
                median=round(median(mark_data)),
                mode=round(mode(mark_data)),
                pass_rate=round(sum(mark >= self.pass_rate for mark in mark_data) / len(marks) * 100),
                first_bucket=len([mark for mark in mark_data if mark <= 40]),
                second_bucket=len([mark for mark in mark_data if 40 <= mark <= 49]),
                third_bucket=len([mark for mark in mark_data if 50 <= mark <= 59]),
                fourth_bucket=len([mark for mark in mark_data if 60 <= mark <= 69]),
                fifth_bucket=len([mark for mark in mark_data if 70 <= mark <= 100]),
            )
        else:
            marks_statistics = MarksStatistics(
                mean=-1,
                median=-1,
                mode=-1,
                pass_rate=-1,
                first_bucket=-1,
                second_bucket=-1,
                third_bucket=-1,
                fourth_bucket=-1,
                fifth_bucket=-1,
            )

        return marks_statistics
