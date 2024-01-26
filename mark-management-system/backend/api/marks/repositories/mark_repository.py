from typing import List

from api.system.models.models import Marks, Class, Student, Degree

from api.system.schemas.schemas import MarksRow
from api.system.schemas.schemas import MarksEdit


class MarkRepository:
    def __init__(self, db):
        self.db = db
    
    def add(self, marks: Marks) -> None:
        self.db.add(marks)
        self.db.commit()
        self.db.refresh(marks)

    def find_by_unique_id(self, marks_id: int) -> Marks:
        return self.db.query(Marks).filter_by(id=marks_id).first()

    def find_by_unique_code(self, marks_unique_code: str) -> Marks:
        return self.db.query(Marks).filter_by(unique_code=marks_unique_code).first()

    def get_student_marks_for_lecturer(self, lecturer_id: int) -> List[MarksRow]:
        return (self.db.query(Class.code, Student.reg_no, Marks.mark, Student.student_name, Degree.level, Degree.name,Marks.unique_code)
            .join(Marks, Marks.class_id == Class.id)
            .join(Student, Student.id == Marks.student_id)
            .join(Degree, Degree.id == Student.degree_id)
            .filter(Class.lecturer_id == lecturer_id)
            .all()
        )
    
    def update(self, mark: Marks, request: MarksEdit) -> None:
        mark.mark = request.mark

        self.db.commit()

    def delete(self, mark: Marks) -> None:
        self.db.delete(mark)
        self.db.commit()
