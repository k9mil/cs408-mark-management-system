from statistics import mean, mode, median

from typing import Tuple

from api.system.schemas.schemas import MarksStatistics

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetGlobalStudentStatisticsUseCase:
    """
    The Use Case containing business logic for retrieving and calculating all student marks in the system.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, current_user: Tuple[str, bool, bool]) -> MarksStatistics:
        """
        Executes the Use Case to retrieve all marks from the system and perform calculations on them.

        Args:
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user (from the JWT) cannot be found.
            PermissionError: If the requestor is not a lecturer or an administrator.
            MarkNotFound: If no marks can be found for the lecturer.
        
        Returns:
            MarksStatistics: A MarksStatistics schema object containing all statistics about the marks in the system.
        """
        user_email, is_lecturer, is_admin = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")

        if not (is_lecturer or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        marks = self.mark_repository.get_all_student_marks()

        if not marks:
            raise MarkNotFound("No marks found in the system")
        
        mark_data = []

        for current_mark in marks:
            mark_data.append(current_mark.mark)

        marks_statistics = MarksStatistics(
            mean=round(mean(mark_data)),
            median=round(median(mark_data)),
            mode=round(mode(mark_data)),
            pass_rate=round(sum(mark >= self.pass_rate for mark in mark_data) / len(marks) * 100),
            first_bucket=len([mark for mark in mark_data if mark <= 19]),
            second_bucket=len([mark for mark in mark_data if 20 <= mark <= 39]),
            third_bucket=len([mark for mark in mark_data if 40 <= mark <= 59]),
            fourth_bucket=len([mark for mark in mark_data if 60 <= mark <= 79]),
            fifth_bucket=len([mark for mark in mark_data if 80 <= mark <= 100]),
        )

        return marks_statistics
