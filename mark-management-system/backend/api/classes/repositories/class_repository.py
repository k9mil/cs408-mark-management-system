from typing import List, Optional

from sqlalchemy.orm import Session

from api.system.models.models import Class
from api.system.models.models import Student
from api.system.models.models import User
from api.system.models.models import Marks

from api.system.schemas.schemas import ClassEdit
from api.system.schemas.schemas import MarksStatistics


class ClassRepository:
    """The repository layer which performs queries and operations on the database for `Class` objects."""

    def __init__(self, db: Session) -> None:
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db
    
    def add(self, class_: Class) -> None:
        """
        Adds an object into the database.

        Args:
            class_: The object to be added.
        """
        self.db.add(class_)
        self.db.commit()
        self.db.refresh(class_)

    def find_by_id(self, class_id: int) -> Optional[Class]:
        """
        Retrieves a class by a given identifier.

        Args:
            class_id: The class id.
        
        Returns:
            Optional[Class]: A `Class` object from the database, however can also return `None` if not found.
        """
        return self.db.query(Class).filter_by(id=class_id).first()

    def find_by_code(self, code: str) -> Optional[Class]:
        """
        Retrieves a class by a given class code.

        Args:
            code: The class code.
        
        Returns:
            Optional[Class]: A `Class` object from the database, however can also return `None` if not found.
        """
        return self.db.query(Class).filter_by(code=code).first()

    def get_class(self, class_id: int) -> Optional[Class]:
        """
        Retrieves a class by a given class identifier.

        Args:
            class_id: The class identifier.
        
        Returns:
            Optional[Class]: A `Class` object from the database, however can also return `None` if not found.
        """
        return self.db.query(Class).filter_by(id=class_id).first()

    def get_classes(self, skip: int = 0, limit: int = 100) -> List[Class]:
        """
        Retrieves a list of classes, given a skip and a limit.

        Args:
            skip: The amount to skip.
            limit: The maximum number of items to be retrieved.
        
        Returns:
            List[Class]: A list of `Class`(es) from the database, however can also return `[]` if none are found.
        """
        return self.db.query(Class).offset(skip).limit(limit).all()
    
    def get_classes_by_lecturer_id(self, lecturer_id: int, skip: int = 0, limit: int = 100) -> List[Class]:
        """
        Retrieves a list of classes, given a lecturer_id, skip and a limit.

        Args:
            lecturer_id: The identifier of the lecturer.
            skip (default: 0): The amount to skip.
            limit (default: 100): The maximum number of items to be retrieved.
        
        Returns:
            List[Class]: A list of `Class`(es) from the database, however can also return `[]` if none are found.
        """
        return self.db.query(Class).filter_by(lecturer_id=lecturer_id).offset(skip).limit(limit).all()
    
    def check_class_code_exists(self, request: ClassEdit) -> bool:
        """
        Checks if a given class code exists in the database.

        Args:
            request: An object that conforms with the `ClassEdit` schema.
        
        Returns:
            bool: True if exists, false if it does not.
        """
        return self.db.query(Class).filter_by(code=request.code).first() is not None

    def is_lecturer_of_class(self, lecturer_id: int, class_id: int) -> bool:
        """
        Checks if a lecturer is the lecturer of a class.

        Args:
            lecturer_id: The identifier of the lecturer.
            class_id: The identifier of the class.
        
        Returns:
            bool: True if they are a lecturer, false if not.
        """
        return self.db.query(Class).filter_by(id=class_id, lecturer_id=lecturer_id).first() is not None
    
    def is_student_in_class_by_ids(self, class_id: int, student_id: int) -> bool:
        """
        Checks if a student belongs to a class.

        Args:
            class_id: The identifier of the class.
            student_id: The identifier of the student.
        
        Returns:
            bool: True if they belong to the class, false if not.
        """
        return self.db.query(Class).join(Class.students).filter(Student.id == student_id, Class.id == class_id).first() is not None
    
    def is_student_in_class(self, class_code: str, reg_no: str) -> bool:
        """
        Checks if a student belongs to a class.

        Args:
            class_code: The identifier of the class.
            reg_no: The identifier of the student.
        
        Returns:
            bool: True if they belong to the class, false if not.
        """
        return self.db.query(Class).join(Class.students).filter(Student.reg_no == reg_no, Class.code == class_code).first() is not None
    
    def get_marks_for_class(self, class_code: str) -> List[MarksStatistics]:
        """
        Retrieves a list of marks for a given class.

        Args:
            class_code: The class for which the student marks should be retrieved.
        
        Returns:
            List[MarksStatistics]: A list of `MarksStatistics` schematic objects.
        """
        return (self.db.query(Class.code, Marks.mark)
            .join(Marks, Marks.class_id == Class.id)
            .filter(Class.code == class_code)
            .all()
        )


    def update(self, class_: Class, lecturer: User, request: ClassEdit) -> None:
        """
        Updates the details of an existing class.

        Args:
            class_: A class object, which already exists in the database.
            lecturer: A user object, the lecturer of the class.
            request: An object that conforms with the `ClassEdit` schema, containing the new information of the class.
        """
        class_.name = request.name
        class_.code = request.code
        class_.credit = request.credit
        class_.credit_level = request.credit_level
        class_.lecturer_id = request.lecturer_id
        class_.lecturer = lecturer

        self.db.commit()

    def delete(self, class_: Class) -> None:
        """
        Deletes an existing class.

        Args:
            class_: A class object, which already exists in the database.
        """
        self.db.delete(class_)
        self.db.commit()
