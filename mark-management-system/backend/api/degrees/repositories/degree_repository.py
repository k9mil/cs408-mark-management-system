from api.system.models.models import Degree


class DegreeRepository:
    def __init__(self, db):
        self.db = db
    
    def add(self, degree: Degree) -> None:
        self.db.add(degree)
        self.db.commit()
        self.db.refresh(degree)

    def find_by_id(self, degree_id: int) -> Degree:
        return self.db.query(Degree).filter_by(id=degree_id).first()

    def find_by_name(self, degree_name: int) -> Degree:
        return self.db.query(Degree).filter_by(name=degree_name).first()
