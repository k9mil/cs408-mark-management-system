from typing import Tuple

from api.system.schemas.schemas import StudentStatistics

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentStatisticsUseCase:
    """
    The Use Case containing business logic for calculating a student's statistics.
    """
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository) -> None:
        self.student_repository = student_repository
        self.user_repository = user_repository
        self.pass_rate = 40
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> StudentStatistics:
        """
        Executes the Use Case to retrieve a a students data, and calculate a few statistics from that data.

        Args:
            reg_no: The unique identifier for the student, the registration number.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user (from the JWT) cannot be found.
            MarkNotFound: If no marks are found for the student.
        
        Returns:
            StudentStatistics: A StudentStatistics schema object containing calculated statistics about the student, i.e. the mean, max mark, min mark and pass rate.
        """
        user_email, _, _ = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        marks_for_student = self.student_repository.get_marks_and_details_for_student(reg_no)

        if not marks_for_student:
            raise MarkNotFound("No marks found for the student")
        
        print(marks_for_student)

        marks = [mark[7] for mark in marks_for_student if mark[7] is not None]
        weights = [marks_for_student[i][4] for i, mark in enumerate(marks_for_student) if mark[7] is not None]

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
