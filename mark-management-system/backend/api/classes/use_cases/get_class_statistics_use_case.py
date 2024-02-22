from statistics import mean, mode, median

from typing import Tuple

from api.system.schemas.schemas import MarksStatistics

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetClassStatisticsUseCase:
    def __init__(self, class_repository: ClassRepository, user_repository: UserRepository):
        self.class_repository = class_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> MarksStatistics:
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marks = self.class_repository.get_marks_for_class(reg_no)

        if marks is None:
            raise MarkNotFound("No marks found for the class")

        mark_data = []

        for current_mark in marks:
            mark_data.append(current_mark[1])

        if mark_data:
            marks_statistics = MarksStatistics(
                mean=round(mean(mark_data)),
                median=round(median(mark_data)),
                mode=round(mode(mark_data)),
                pass_rate=round(sum(mark >= self.pass_rate for mark in mark_data) / len(marks) * 100),
            )
        else:
            marks_statistics = MarksStatistics(
                mean=-1,
                median=-1,
                mode=-1,
                pass_rate=-1,
            )

        return marks_statistics
