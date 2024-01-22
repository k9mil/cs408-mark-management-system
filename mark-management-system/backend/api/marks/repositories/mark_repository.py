from api.system.models.models import Marks


class MarkRepository:
    def __init__(self, db):
        self.db = db
    
    def add(self, marks: Marks) -> None:
        self.db.add(marks)
        self.db.commit()
        self.db.refresh(marks)

    def find_by_unique_id(self, marks_id: int) -> Marks:
        return self.db.query(Marks).filter_by(id=marks_id).first()

    def find_by_unique_code(self, marks_unique_code: int) -> Marks:
        return self.db.query(Marks).filter_by(unique_code=marks_unique_code).first()
