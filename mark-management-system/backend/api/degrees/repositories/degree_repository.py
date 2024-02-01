from typing import Optional, List

from sqlalchemy.orm import Session

from api.system.models.models import Class
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
