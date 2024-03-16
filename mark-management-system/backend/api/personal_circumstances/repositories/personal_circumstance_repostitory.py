from typing import List

from sqlalchemy.orm import Session

from api.system.models.models import PersonalCircumstance

from api.system.schemas.schemas import PersonalCircumstancesCreate
from api.system.schemas.schemas import PersonalCircumstancesBase


class PersonalCircumstanceRepository:
    """The repository layer which performs queries and operations on the database for `PersonalCircumstanc` objects."""

    def __init__(self, db: Session) -> None:
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db
    
    def add(self, personal_circumstance: PersonalCircumstancesBase) -> None:
        """
        Adds an object into the database.

        Args:
            personal_circumstance: The object to be added.
        """
        self.db.add(personal_circumstance)
        self.db.commit()
        self.db.refresh(personal_circumstance)

    def find_by_details(self, request: PersonalCircumstancesCreate, student_id: int) -> List[PersonalCircumstance]:
        """
        Checks whether a given request is already in the database.

        Args:
            request: The request containing information that was passed in to create the personal circumstances.
            student_id: Identifier of the student in the request.
        
        Returns:
            Optional[PersonalCircumstance]: The first result from the database that matches the filter, otherwise None.
        """
        return self.db.query(PersonalCircumstance).filter_by(
            details=request.details,
            semester=request.semester,
            cat=request.cat,
            comments=request.comments,
            student_id=student_id,
        ).first()

    def get_by_student_id(self, student_id: int) -> List[PersonalCircumstance]:
        """
        Get a list of personal circumstances by an id of a student.

        Args:
            student_id: The student identificator.
        
        Returns:
            Optional[PersonalCircumstance]: A List[PersonalCircumstance] from the database.
        """
        return self.db.query(PersonalCircumstance).filter_by(student_id=student_id).all()
