from statistics import mean, mode, median

from typing import Tuple

from api.system.schemas.schemas import MarksStatistics

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentStatisticsUseCase:
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository):
        self.mark_repository = mark_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, current_user: Tuple[str, bool, bool]) -> MarksStatistics:
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marks = self.mark_repository.get_student_marks_for_lecturer(user.id)

        if marks is None:
            raise MarkNotFound("No results found for the lecturer")
        
        mark_data = []

        for current_mark in marks:
            mark_data.append(current_mark[6])

        marks_statistics = MarksStatistics(
            mean=round(mean(mark_data)),
            median=round(median(mark_data)),
            mode=round(mode(mark_data)),
            pass_rate=round(sum(mark >= self.pass_rate for mark in mark_data) / len(marks) * 100),
        )

        return marks_statistics
