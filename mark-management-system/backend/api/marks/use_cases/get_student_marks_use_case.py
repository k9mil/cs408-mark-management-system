from typing import Tuple, List

from api.system.schemas.schemas import MarksRow

from api.marks.repositories.mark_repository import MarkRepository
from api.users.repositories.user_repository import UserRepository

from api.marks.errors.mark_not_found import MarkNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentMarksUseCase:
    def __init__(self, mark_repository: MarkRepository, user_repository: UserRepository):
        self.mark_repository = mark_repository
        self.user_repository = user_repository
    
    def execute(self, current_user: Tuple[str, bool, bool]) -> List[MarksRow]:
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        marks = self.mark_repository.get_student_marks_for_lecturer(user.id)

        if marks is None:
            raise MarkNotFound("No results found for the lecturer")
        
        marks_row = []

        for current_mark in marks:
            mark_row = MarksRow(
                id=current_mark[0],
                student_name=current_mark[1],
                reg_no=current_mark[2],
                class_code=current_mark[3],
                degree_level=current_mark[4],
                degree_name=current_mark[5],
                unique_code=current_mark[6],
                mark=current_mark[7],
            )
            
            marks_row.append(mark_row)

        return marks_row
