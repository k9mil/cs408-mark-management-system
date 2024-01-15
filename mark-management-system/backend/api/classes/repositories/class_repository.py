from api.system.models.models import Class

from api.utils.singleton import singleton


@singleton
class ClassRepository:
    def __init__(self, db):
        self.db = db
    
    def add(self, class_: Class) -> None:
        self.db.add(class_)
        self.db.commit()
        self.db.refresh(class_)

    def find_by_code(self, code: int) -> Class:
        return self.db.query(Class).filter_by(code=code).first()
