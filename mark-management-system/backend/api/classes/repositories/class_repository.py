from typing import List, Optional

from sqlalchemy.orm import Session

from api.system.models.models import Class
from api.system.models.models import User

from api.system.schemas.schemas import ClassEdit


class ClassRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def add(self, class_: Class) -> None:
        self.db.add(class_)
        self.db.commit()
        self.db.refresh(class_)

    def find_by_code(self, code: str) -> Optional[Class]:
        return self.db.query(Class).filter_by(code=code).first()

    def get_class(self, class_id: int) -> Optional[Class]:
        return self.db.query(Class).filter_by(id=class_id).first()

    def get_classes(self, skip: int, limit: int) -> List[Class]:
        return self.db.query(Class).offset(skip).limit(limit).all()
    
    def get_classes_by_lecturer_id(self, lecturer_id: int, skip: int = 0, limit: int = 100) -> List[Class]:
        return self.db.query(Class).filter_by(lecturer_id=lecturer_id).offset(skip).limit(limit).all()
    
    def check_class_code_exists(self, request: ClassEdit) -> bool:
        return self.db.query(Class).filter_by(code=request.code).first() is not None

    def update(self, class_: Class, lecturer: User, request: ClassEdit) -> None:
        class_.name = request.name
        class_.code = request.code
        class_.credit = request.credit
        class_.credit_level = request.credit_level
        class_.lecturer_id = request.lecturer_id
        class_.lecturer = lecturer

        self.db.commit()

    def delete(self, class_: Class) -> None:
        self.db.delete(class_)
        self.db.commit()
