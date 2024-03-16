from typing import List

from sqlalchemy.orm import Session

from api.system.models.models import AcademicMisconduct

from api.system.schemas.schemas import AcademicMisconductBase




class AcademicMisconductRepository:
    """The repository layer which performs queries and operations on the database for `AcademicMisconduct` objects."""

    def __init__(self, db: Session) -> None:
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db
    
    def add(self, academic_misconduct: AcademicMisconductBase) -> None:
        """
        Adds an object into the database.

        Args:
            academic_misconduct: The object to be added.
        """
        self.db.add(academic_misconduct)
        self.db.commit()
        self.db.refresh(academic_misconduct)

    def get_by_student_id(self, student_id: int) -> List[AcademicMisconduct]:
        """
        Get a list of academic misconducts by an id of a student.

        Args:
            student_id: The student identificator.
        
        Returns:
            Optional[AcademicMisconduct]: A List[AcademicMisconduct] from the database.
        """
        return self.db.query(AcademicMisconduct).filter_by(student_id=student_id).all()
