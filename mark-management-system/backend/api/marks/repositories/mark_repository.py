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

    def find_by_unique_id(self, marks_id: int) -> Optional[Marks]:
        """
        Retrieves a mark by a given mark identifier.

        Args:
            marks_id: The mark identifier.
        
        Returns:
            Optional[Marks]: A `Marks` from the database, however can also return `None` if not found.
        """
        return self.db.query(Marks).filter_by(id=marks_id).first()

    def find_by_unique_code(self, marks_unique_code: str) -> Marks:
        """
        Retrieves a mark by a given mark identifier.

        Args:
            marks_unique_code: The mark identifier.
        
        Returns:
            Optional[Marks]: A `Marks` from the database, however can also return `None` if not found.
        """
        return self.db.query(Marks).filter_by(unique_code=marks_unique_code).first()

    def get_student_marks_for_lecturer(self, lecturer_id: int) -> List[MarksRow]:
        """
        Retrieves a list of student marks for a particular lecturer.

        Args:
            lecturer_id: The lecturer for which the student marks should be retrieved.
        
        Returns:
            List[MarksRow]: A list of `MarksRow` schematic objects.
        """
        return (self.db.query(Student.id, Student.student_name, Student.reg_no, Class.code, Degree.level, Degree.name, Marks.unique_code, Marks.mark)
            .join(Marks, Marks.class_id == Class.id)
            .join(Student, Student.id == Marks.student_id)
            .join(Degree, Degree.id == Student.degree_id)
            .filter(Class.lecturer_id == lecturer_id)
            .all()
        )
    
    def get_marks_for_student(self, reg_no: str) -> List[MarksRow]:
        """
        Retrieves a list of student marks for a particular student.

        Args:
            reg_no: The student for which the student marks should be retrieved.
        
        Returns:
            List[MarksRow]: A list of `MarksRow` schematic objects.
        """
        return (self.db.query(Student.id, Student.student_name, Student.reg_no, Class.code, Degree.level, Degree.name, Marks.unique_code, Marks.mark)
            .join(Marks, Marks.class_id == Class.id)
            .join(Student, Student.id == Marks.student_id)
            .join(Degree, Degree.id == Student.degree_id)
            .filter(Student.reg_no == reg_no)
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
