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

    def get_classes(self, skip: int, limit: int) -> list[Class]:
        return self.db.query(Class).offset(skip).limit(limit).all()
    
    def get_classes_by_lecturer_id(self, lecturer_id: int, skip: int, limit: int) -> list[Class]:
        return self.db.query(Class).filter_by(lecturer_id=lecturer_id).offset(skip).limit(limit).all()
