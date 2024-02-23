from typing import List, Optional

from sqlalchemy.orm import Session

from api.system.models.models import Marks, Class, Student, Degree

from api.system.schemas.schemas import MarksRow
from api.system.schemas.schemas import MarksEdit


class MarkRepository:
    """The repository layer which performs queries and operations on the database for `Marks` objects."""

    def __init__(self, db: Session):
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db
    
    def add(self, marks: Marks) -> None:
        """
        Adds an object into the database.

        Args:
            marks: The object to be added.
        """
        self.db.add(marks)
        self.db.commit()
        self.db.refresh(marks)

    def find_by_id(self, mark_id: int) -> Optional[Marks]:
        """
        Retrieves a mark by a given mark identifier.

        Args:
            marks_id: The mark identifier.
        
        Returns:
            Optional[Marks]: A `Marks` from the database, however can also return `None` if not found.
        """
        return self.db.query(Marks).filter_by(id=mark_id).first()

    def find_by_student_id_and_class_id(self, student_id: int, class_id: int) -> Optional[Marks]:
        """
        Retrieves a mark by a student_id and a

        Args:
            marks_id: The mark identifier.
        
        Returns:
            Optional[Marks]: A `Marks` from the database, however can also return `None` if not found.
        """
        return self.db.query(Marks).filter_by(student_id=student_id, class_id=class_id).first()

    def get_student_marks_for_lecturer(self, lecturer_id: int) -> List[MarksRow]:
        """
        Retrieves a list of student marks for a particular lecturer.

        Args:
            lecturer_id: The lecturer for which the student marks should be retrieved.
        
        Returns:
            List[MarksRow]: A list of `MarksRow` schematic objects.
        """
        return (self.db.query(Marks.id, Student.student_name, Student.reg_no, Class.code, Degree.level, Degree.name, Marks.mark)
            .join(Marks, Marks.class_id == Class.id)
            .join(Student, Student.id == Marks.student_id)
            .join(Degree, Degree.id == Student.degree_id)
            .filter(Class.lecturer_id == lecturer_id)
            .all()
        )
    
    def get_all_student_marks(self) -> List[Marks]:
        """
        Retrieves a list of all student marks.
        
        Returns:
            List[Marks]: A list of `Marks` objects.
        """
        return self.db.query(Marks).all()
    
    def get_marks_for_student(self, reg_no: str) -> List[MarksRow]:
        """
        Retrieves a list of student marks for a particular student.

        Args:
            reg_no: The student for which the student marks should be retrieved.
        
        Returns:
            List[MarksRow]: A list of `MarksRow` schematic objects.
        """
        return (self.db.query(Student.id, Student.student_name, Student.reg_no, Class.code, Class.name, Degree.level, Degree.name, Marks.mark)
            .join(Marks, Marks.class_id == Class.id)
            .join(Student, Student.id == Marks.student_id)
            .join(Degree, Degree.id == Student.degree_id)
            .filter(Student.reg_no == reg_no)
            .all()
        )
    
    def get_student_marks_for_class_as_marks_row(self, class_code: str) -> List[MarksRow]:
        """
        Retrieves a list of student marks for a particular class code.

        Args:
            class_code: The class code for which the marks should be retrieved.
        
        Returns:
            List[MarksRow]: A list of `MarksRow` schematic objects.
        """
        return (self.db.query(Student.id, Student.student_name, Student.reg_no, Class.code, Class.name, Degree.level, Degree.name, Marks.mark)
            .join(Marks, Marks.class_id == Class.id)
            .join(Student, Student.id == Marks.student_id)
            .join(Degree, Degree.id == Student.degree_id)
            .filter(Class.code == class_code)
            .all()
        )
    
    def get_student_marks_for_class(self, class_id: int) -> List[Marks]:
        """
        Retrieves a list of student marks for a particular class.

        Args:
            class_id: The class identifier.
        
        Returns:
            List[Marks]: A list of `Marks` objects from the database.
        """
        return self.db.query(Marks).filter_by(class_id=class_id).all()
    
    def update(self, mark: Marks, request: MarksEdit) -> None:
        """
        Updates the details of an existing mark.

        Args:
            mark: A mark object, which already exists in the database.
            request: An object that conforms with the `MarksEdit` schema, containing the new information of the mark.
        """
        mark.mark = request.mark

        self.db.commit()

    def delete(self, mark: Marks) -> None:
        """
        Deletes an existing mark.

        Args:
            mark: A mark object, which already exists in the database.
        """
        self.db.delete(mark)
        self.db.commit()
