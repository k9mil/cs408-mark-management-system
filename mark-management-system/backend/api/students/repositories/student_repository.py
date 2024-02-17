from typing import List, Optional

from sqlalchemy.orm import Session

from api.system.models.models import Student
from api.system.models.models import Class
from api.system.models.models import Marks
from api.system.models.models import Degree

from api.system.schemas.schemas import StudentBase
from api.system.schemas.schemas import StudentStatistics


class StudentRepository:
    """The repository layer which performs queries and operations on the database for `Student` objects."""

    def __init__(self, db: Session) -> None:
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db
    
    def add(self, student: Student) -> None:
        """
        Adds an object into the database.

        Args:
            student: The object to be added.
        """
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)

    def find_by_reg_no(self, reg_no: str) -> Optional[Student]:
        """
        Retrieves a class by a given registration number.

        Args:
            reg_no: The registration number.
        
        Returns:
            Optional[Student]: A `Student` object from the database, however can also return `None` if not found.
        """
        return self.db.query(Student).filter_by(reg_no=reg_no).first()

    def find_by_id(self, student_id: int) -> Optional[Student]:
        """
        Retrieves a class by a given student id.

        Args:
            student_id: The student id.
        
        Returns:
            Optional[Student]: A `Student` object from the database, however can also return `None` if not found.
        """
        return self.db.query(Student).filter_by(id=student_id).first()

    def get_students(self, skip: int, limit: int) -> List[StudentBase]:
        """
        Retrieves a list of classes, given a skip and a limit.

        Args:
            skip: The amount to skip.
            limit: The maximum number of items to be retrieved.
        
        Returns:
            List[Student]: A list of `Student`(s) from the database, however can also return `[]` if none are found.
        """
        return self.db.query(Student).offset(skip).limit(limit).all()

    def get_marks_and_details_for_student(self, reg_no: str) -> List[StudentStatistics]:
        """
        Retrieves a list of student marks alongside their details.

        Args:
            reg_no: The student for which the student marks should be retrieved.
        
        Returns:
            List[StudentStatistics]: A list of `StudentStatistics` schematic objects.
        """
        return (self.db.query(Student.id, Student.student_name, Student.reg_no, Class.code, Degree.level, Degree.name, Marks.mark)
            .join(Marks, Marks.class_id == Class.id)
            .join(Student, Student.id == Marks.student_id)
            .join(Degree, Degree.id == Student.degree_id)
            .filter(Student.reg_no == reg_no)
            .all()
        )
