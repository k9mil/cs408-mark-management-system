from api.system.models.models import Student


class StudentRepository:
    def __init__(self, db):
        self.db = db
    
    def add(self, student: Student) -> None:
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)

    def find_by_reg_no(self, reg_no: int) -> Student:
        return self.db.query(Student).filter_by(reg_no=reg_no).first()

    def find_by_id(self, student_id: int) -> Student:
        return self.db.query(Student).filter_by(id=student_id).first()

    def get_students(self, skip: int, limit: int) -> list[Student]:
        return self.db.query(Student).offset(skip).limit(limit).all()
