from statistics import mean, mode, median

from typing import Tuple

from api.system.schemas.schemas import MarksStatistics

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentStatisticsUseCase:
    """
    The Use Case containing business logic for retrieving and calculating student marks for a particular
    lecturer.
    """
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository) -> None:
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, current_user: Tuple[str, bool, bool]) -> MarksStatistics:
        """
        Executes the Use Case to retrieve marks for a lecturer and calculate statistics.

        Args:
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            MarkNotFound: If no marks can be found for the lecturer.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            MarksStatistics: A MarksStatistics schema object containing all statistics about the uploaded marks of the lecturer (requestor).
        """
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marks = self.mark_repository.get_student_marks_for_lecturer(user.id)

        if not marks:
            raise MarkNotFound("No results found for the lecturer")
        
        mark_data = []

        for current_mark in marks:
            mark_data.append(current_mark[6])

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

        return marks_statistics
