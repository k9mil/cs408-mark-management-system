from typing import Optional

from sqlalchemy.orm import Session

from api.system.models.models import Degree
from api.system.models.models import DegreeClasses


class DegreeRepository:
    """The repository layer which performs queries and operations on the database for `Degree` objects."""

    def __init__(self, db: Session) -> None:
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db
    
    def add(self, degree: Degree) -> None:
        """
        Adds an object into the database.

        Args:
            degree: The object to be added.
        """
        self.db.add(degree)
        self.db.commit()
        self.db.refresh(degree)

    def find_by_id(self, degree_id: int) -> Optional[Degree]:
        """
        Retrieves a degree by a given degree_id.

        Args:
            degree_id: The degree identifier.
        
        Returns:
            Optional[Degree]: A `Degree` from the database, however can also return `None` if not found.
        """
        return self.db.query(Degree).filter_by(id=degree_id).first()

    def find_by_name(self, degree_name: str) -> Optional[Degree]:
        """
        Retrieves a degree by a given degree_name.

        Args:
            degree_name: The degree name.
        
        Returns:
            Optional[Degree]: A `Degree` from the database, however can also return `None` if not found.
        """
        return self.db.query(Degree).filter_by(name=degree_name).first()
    
    def find_by_name_and_level(self, degree_name: str, degree_level: str) -> Optional[Degree]:
        """
        Retrieves a degree by both a given degree_name and a degree_level.

        Args:
            degree_name: The degree name.
            degree_level: The degree level.
        
        Returns:
            Optional[Degree]: A `Degree` from the database, however can also return `None` if not found.
        """
        return self.db.query(Degree).filter_by(name=degree_name, level=degree_level).first()
    
    def is_class_associated_with_degree(self, degree_id: int, class_id: int) -> Optional[DegreeClasses]:
        """
        Performs a check if a particular class is associated with a particular degree.

        Args:
            degree_id: The degree identifier.
            class_id: The class identifier.
        
        Returns:
            Optional[DegreeClasses]: A `DegreeClasses` from the database, however can also return `None` if not found.
        """
        return self.db.query(DegreeClasses).filter_by(degree_id=degree_id, class_id=class_id).first()
