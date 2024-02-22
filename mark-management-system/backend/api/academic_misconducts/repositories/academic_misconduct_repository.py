from typing import Optional

from sqlalchemy.orm import Session

from api.system.models.models import AcademicMisconduct

from api.system.schemas.schemas import AcademicMisconductBase
from api.system.schemas.schemas import AcademicMisconductCreate


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

    def find_by_details(self, request: AcademicMisconductCreate) -> Optional[AcademicMisconduct]:
        """
        Checks whether a given request is already in the database.

        Args:
            request: The request containing information that was passed in to create the academic misconduct.
        
        Returns:
            Optional[AcademicMisconduct]: The first result from the database that matches the filter, otherwise None.
        """
        return self.db.query(AcademicMisconduct).filter_by(
            date=request.date,
            outcome=request.outcome,
            student_reg_no=request.reg_no,
            class_code=request.class_code,
        ).first()
