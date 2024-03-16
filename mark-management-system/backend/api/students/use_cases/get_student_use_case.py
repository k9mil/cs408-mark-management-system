from typing import Tuple, List

from api.system.models.models import Student
from api.system.models.models import Degree
from api.system.models.models import PersonalCircumstance

from api.system.schemas.schemas import Student as StudentSchema
from api.system.schemas.schemas import ClassWithMisconduct
from api.system.schemas.schemas import AcademicMisconductCreate
from api.system.schemas.schemas import DegreeBase
from api.system.schemas.schemas import PersonalCircumstancesBase

from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository
from api.classes.repositories.class_repository import ClassRepository

from api.students.errors.student_not_found import StudentNotFound

from api.users.errors.user_not_found import UserNotFound


class GetStudentUseCase:
    """
    The Use Case containing business logic for retrieving a student.
    """
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository, class_repository: ClassRepository) -> None:
        self.student_repository = student_repository
        self.user_repository = user_repository
        self.class_repository = class_repository
    
    def execute(self, reg_no: str, current_user: Tuple[str, bool, bool]) -> StudentSchema:
        """
        Executes the Use Case to retrieve a student from the system, given a registration number.

        Args:
            reg_no: The unique identifier for the student, the registration number.
            current_user: A middleware object `current_user` which contains JWT information. For more details see the controller.

        Raises:
            PermissionError: If the user is not a user and a lecturer, or an administrator.
            StudentNotFound: If the student cannot be found, given the identifier.
            UserNotFound: If the user (from the JWT) cannot be found.
        
        Returns:
            StudentSchema: A StudentSchema schema object containing all information about the student.
        """
        user_email, is_admin, is_lecturer = current_user

        user = self.user_repository.find_by_email(user_email)
        
        if user is None:
            raise UserNotFound("User not found")

        if not ((user and is_lecturer) or is_admin):
            raise PermissionError("Permission denied to access this resource")
        
        student = self.student_repository.find_by_reg_no(reg_no)

        if student is None:
            raise StudentNotFound("Student not found")

        return StudentSchema(
            id=student.id,
            reg_no=student.reg_no,
            student_name=student.student_name,
            classes=self.construct_classes_with_academic_misconduct(student),
            personal_circumstances=self.construct_personal_circumstances(student.personal_circumstances),
            year=student.year,
            degree_id=student.degree_id,
            degree=self.construct_degree(student.degree),
        )

    def construct_classes_with_academic_misconduct(self, student: Student) -> List[ClassWithMisconduct]:
        classes_with_academic_misconduct = []

        for class_ in student.classes:
            academic_misconducts = []

            for misconduct in class_.academic_misconducts:
                if misconduct.student_id == student.id:
                    class_ = self.class_repository.find_by_id(misconduct.class_id)

                    misconduct_item = AcademicMisconductCreate(
                        reg_no=student.reg_no,
                        class_code=class_.code,
                        date=misconduct.date,
                        outcome=misconduct.outcome,
                    )

                    academic_misconducts.append(misconduct_item)
            
            class_with_misconduct = ClassWithMisconduct(
                name=class_.name,
                code=class_.code,
                credit=class_.credit,
                credit_level=class_.credit_level,
                academic_misconducts=academic_misconducts
            )
        
            classes_with_academic_misconduct.append(class_with_misconduct)

        return classes_with_academic_misconduct

    def construct_personal_circumstances(self, personal_circumstances: PersonalCircumstance) -> List[PersonalCircumstancesBase]:
        personal_circumstances = []

        for circumstance in personal_circumstances:
            personal_circumstance = PersonalCircumstancesBase(
                details=circumstance.details,
                semester=circumstance.semester,
                cat=circumstance.cat,
                comments=circumstance.comments,
            )

            personal_circumstances.append(personal_circumstance)

        return personal_circumstances

    def construct_degree(self, degree: Degree) -> DegreeBase:
        return DegreeBase(
            level=degree.level,
            name=degree.name,
            code=degree.code,
        )
