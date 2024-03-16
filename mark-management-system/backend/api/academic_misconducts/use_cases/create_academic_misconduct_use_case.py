from typing import Tuple

from api.system.models.models import AcademicMisconduct

from api.system.schemas.schemas import AcademicMisconductBase as AcademicMisconductSchema
from api.system.schemas.schemas import AcademicMisconductCreate

from api.academic_misconducts.repositories.academic_misconduct_repository import AcademicMisconductRepository

from api.users.repositories.user_repository import UserRepository
from api.students.repositories.student_repository import StudentRepository
from api.classes.repositories.class_repository import ClassRepository

from api.users.errors.user_not_found import UserNotFound

from api.classes.errors.class_not_found import ClassNotFound

from api.students.errors.student_not_found import StudentNotFound

class CreateAcademicMisconductUseCase:
    """
    The Use Case containing business logic for creating a new academic misconduct.
    """
    def __init__(
            self,
            academic_misconduct_repository: AcademicMisconductRepository,
            user_repository: UserRepository,
            student_repository: StudentRepository,
            class_repository: ClassRepository,
        ) -> None:
        self.academic_misconduct_repository = academic_misconduct_repository
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.class_repository = class_repository

    def execute(self, request: AcademicMisconductCreate, current_user: Tuple[str, bool, bool]) -> AcademicMisconductSchema:
        """
        Executes the Use Case to create a new academic misconduct entry in the system.

        Args:
            request: A `AcademicMisconductCreate` object is required which contains the necessary details for academic misconduct creation.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            UserNotFound: If the user from the JWT token is not found.
            PermissionError: If the user is not valid and a lecturer, or if they are not an administrator.
            StudentNotFound: If the student from the request is not found.
            ClassNotFound: If the class code from the request is not found.
        
        Returns:
            AcademicMisconductSchema: A AcademicMisconductSchema schema object containing all information about the newly created academic misconduct.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)

        if user is None:
            raise UserNotFound("User not found")
        
        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        student = self.student_repository.find_by_reg_no(request.reg_no)
            
        if not student:
            raise StudentNotFound("Student not found")
        
        class_ = self.class_repository.find_by_code(request.class_code)
            
        if not class_:
            raise ClassNotFound("Class not found")
        
        if self.class_repository.is_student_in_class_by_ids(class_.id, student.id) is False:
            raise StudentNotFound("Student doesnt belong to the provided class")

        academic_misconduct = AcademicMisconduct(
            date=request.date,
            outcome=request.outcome,
            student_id=student.id,
            class_id=class_.id,
        )

        self.academic_misconduct_repository.add(academic_misconduct)
        
        return AcademicMisconductSchema(
            date=request.date,
            outcome=request.outcome,
            class_code=class_.code
        )
