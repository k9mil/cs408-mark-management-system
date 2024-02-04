from typing import Optional

from sqlalchemy.orm import Session

from api.system.models.models import Degree
from api.system.models.models import DegreeClasses


class DegreeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def add(self, degree: Degree) -> None:
        self.db.add(degree)
        self.db.commit()
        self.db.refresh(degree)

    def find_by_id(self, degree_id: int) -> Optional[Degree]:
        return self.db.query(Degree).filter_by(id=degree_id).first()

    def find_by_name(self, degree_name: str) -> Optional[Degree]:
        return self.db.query(Degree).filter_by(name=degree_name).first()
    
    def find_by_name_and_level(self, degree_name: str, degree_level: str) -> Optional[Degree]:
        print(degree_name, degree_level)
        return self.db.query(Degree).filter_by(name=degree_name, level=degree_level).first()
    
    def is_class_associated_with_degree(self, degree_id: int, class_id: int) -> bool:
        return self.db.query(DegreeClasses).filter_by(degree_id=degree_id, class_id=class_id).first() is None
