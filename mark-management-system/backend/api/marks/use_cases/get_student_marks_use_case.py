from typing import Tuple, List

from api.system.schemas.schemas import MarksRow

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound


class GetStudentMarksUseCase:
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository):
        self.mark_repository = mark_repository
        self.user_repository = user_repository
    
    def execute(self, current_user: Tuple[str, bool]) -> List[MarksRow]:
        user_email, is_admin = current_user

        lecturer = self.user_repository.find_by_email(user_email)
        
        # if is_admin is False or lecturer is None:
        #     raise PermissionError("Permission denied to access this resource")
        
        marks = self.mark_repository.get_student_marks_for_lecturer(lecturer.id)

        if marks is None:
            raise MarkNotFound("No results found for the lecturer")
        
        marks_row = []

        for current_mark in marks:
            mark_row = MarksRow(
                class_code=current_mark[0],
                reg_no=current_mark[1],
                mark=current_mark[2],
                student_name=current_mark[3],
                degree_level=current_mark[4],
                degree_name=current_mark[5],
                unique_code=current_mark[6],
            )
            
            marks_row.append(mark_row)

        return marks_row
