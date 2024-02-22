from typing import Tuple

from api.system.schemas.schemas import StudentStatistics

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentStatisticsUseCase:
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> StudentStatistics:
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marksForStudent = self.student_repository.get_marks_and_details_for_student(reg_no)

        if marksForStudent is None:
            raise MarkNotFound("No marks found for the student")

        marks = [mark[7] for mark in marksForStudent]
        weights = [mark[4] for mark in marksForStudent]

        if marks:
            weighted_sum = 0
            total_weight = 0

            for (mark, weight) in zip(marks, weights):
                weighted_sum += mark * weight
                total_weight += weight

            marks_statistics = StudentStatistics(
                mean=round(weighted_sum / total_weight),
                max_mark=max(marks),
                min_mark=min(marks),
                pass_rate=round(sum(mark >= self.pass_rate for mark in marks) / len(marks) * 100),
            )
        else:
            marks_statistics = StudentStatistics(
                mean=-1,
                max_mark=-1,
                min_mark=-1,
                pass_rate=-1,
            )

        return marks_statistics
