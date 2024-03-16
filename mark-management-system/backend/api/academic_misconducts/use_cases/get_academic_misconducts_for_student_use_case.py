from typing import Tuple, List

from api.system.schemas.schemas import AcademicMisconductBase as AcademicMisconductSchema

from api.academic_misconducts.repositories.academic_misconduct_repository import AcademicMisconductRepository
from api.users.repositories.user_repository import UserRepository
from api.students.repositories.student_repository import StudentRepository
from api.classes.repositories.class_repository import ClassRepository

from api.users.errors.user_not_found import UserNotFound
from api.students.errors.student_not_found import StudentNotFound

from api.academic_misconducts.errors.academic_misconduct_not_found import AcademicMisconductNotFound


class GetAcademicMisconductsForStudentUseCase:
    """
    The Use Case containing business logic for retrieving all academic misconducts for a student.
    """
    def __init__(self, 
                 academic_misconduct_repository: AcademicMisconductRepository,
                 user_repository: UserRepository,
                 student_repository: StudentRepository,
                 class_repository: ClassRepository,
                ) -> None:
        self.academic_misconduct_repository = academic_misconduct_repository
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.class_repository = class_repository

    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> List[AcademicMisconductSchema]:
        """
        Executes the Use Case to retrieve all academic misconducts for a particular student in the system.

        Args:
            reg_no: The student for which to retrieve the data.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user from the JWT token is not found.
            PermissionError: If the user is not valid and a lecturer, or if they are not an administrator.
            AcademicMisconductNotFound: If no academic misconducts are found.
        
        Returns:
            List[AcademicMisconductSchema]: A list of AcademicMisconductSchema schema objects containing key information about the academic misconducts.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        student = self.student_repository.find_by_reg_no(reg_no)

        if not student:
            raise StudentNotFound("Student not found")
        
        academic_misconducts = self.academic_misconduct_repository.get_by_student_id(student.id)

        if not academic_misconducts:
            raise AcademicMisconductNotFound("No academic misconducts found")
        
        transformed_academic_misconducts = []

        for misconduct in academic_misconducts:
            class_ = self.class_repository.find_by_id(misconduct.class_id)

            academic_misconduct = AcademicMisconductSchema(
                date=misconduct.date,
                outcome=misconduct.outcome,
                class_code=class_.code,
            )

            transformed_academic_misconducts.append(academic_misconduct)

        return transformed_academic_misconducts
