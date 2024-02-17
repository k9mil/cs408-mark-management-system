from statistics import mean, mode, median

from typing import Tuple

from api.system.schemas.schemas import StudentStatistics

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentsDetailsAndStatisticsUseCase:
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> StudentStatistics:
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marks = self.student_repository.get_marks_and_details_for_student(reg_no)

        if marks is None:
            raise MarkNotFound("No marks found for the student")
        
        mark_data = []

        for current_mark in marks:
            mark_data.append(current_mark[6])

        marks_statistics = StudentStatistics(
            reg_no=marks[0][2],
            student_name=marks[0][1],
            degree_level=marks[0][4],
            degree_name=marks[0][5],
            mean=round(mean(mark_data)),
            median=round(median(mark_data)),
            mode=round(mode(mark_data)),
            pass_rate=round(sum(mark >= self.pass_rate for mark in mark_data) / len(marks) * 100),
        )

        return marks_statistics
