import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from sqlalchemy import create_engine

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from api.system.models.models import Base

from api.config import DevelopmentConfig
from api.config import TestingConfig

from api.classes.repositories.class_repository import ClassRepository
from api.degrees.repositories.degree_repository import DegreeRepository
from api.marks.repositories.mark_repository import MarkRepository
from api.personal_circumstances.repositories.personal_circumstance_repostitory import PersonalCircumstanceRepository
from api.roles.repositories.roles_repository import RolesRepository
from api.students.repositories.student_repository import StudentRepository
from api.users.repositories.user_repository import UserRepository
from api.academic_misconducts.repositories.academic_misconduct_repository import AcademicMisconductRepository

from api.system.models.models import Role, Class, Degree, Marks, PersonalCircumstance, Student, User, RoleUsers, AcademicMisconduct

from api.users.hashers.bcrypt_hasher import BCryptHasher


def initialise_roles(db: Session) -> None:
    roles_repository = RolesRepository(db)

    roles_repository.add(Role(id=1, title="admin"))
    roles_repository.add(Role(id=2, title="lecturer"))

def create_degree(db: Session) -> None:
    degree_repository = DegreeRepository(db)

    degree_repository.add(Degree(level="BSc (Hons)", name="Computer Science", code="0403"))
    degree_repository.add(Degree(level="BSc", name="Software Engineering", code="0404"))

def create_students(db: Session) -> None:
    student_repository = StudentRepository(db)

    student_repository.add(Student(reg_no="abc12345", student_name="John Doe", year=1, degree_id=1))
    student_repository.add(Student(reg_no="abc54321", student_name="Jane Doe", year=2, degree_id=1))
    student_repository.add(Student(reg_no="abc33311", student_name="Jack Doe", year=3, degree_id=1))
    student_repository.add(Student(reg_no="abc33355", student_name="Annie Doe", year=4, degree_id=1))

def create_users(db: Session) -> None:
    user_repository = UserRepository(db)
    bcrypt_hasher = BCryptHasher()

    hashed_password = bcrypt_hasher.hash("12345678")

    admin_user = User(
            email_address="admin@mms.com",
            first_name="Camil",
            last_name="Zak",
            password=hashed_password
        )
    
    lecturer_user = User(
            email_address="lecturer@mms.com",
            first_name="Kamil",
            last_name="Zak",
            password=hashed_password
        )
    
    base_user = User(
            email_address="base@mms.com",
            first_name="Kamil",
            last_name="Zack",
            password=hashed_password
        )

    user_repository.add(
        admin_user
    )

    user_repository.add(
        lecturer_user
    )

    user_repository.add(
        base_user
    )

    roles_repository = RolesRepository(db)

    roles_repository.add_user(
        RoleUsers(
            user_id=1,
            role_id=1,
        ),
        admin_user
    )

    roles_repository.add_user(
        RoleUsers(
            user_id=2,
            role_id=2,
        ),
        lecturer_user
    )

def create_classes(db: Session) -> None:
    class_repository = ClassRepository(db)

    class_repository.add(Class(name="Information Access and Mining", code="CS412", credit="20", credit_level="4", lecturer_id=2))
    class_repository.add(Class(name="Computer Security", code="CS407", credit="20", credit_level="4", lecturer_id=2))
    class_repository.add(Class(name="Human-Centred Security", code="CS426", credit="20", credit_level="4", lecturer_id=2))
    class_repository.add(Class(name="Individual Project", code="CS408", credit="40", credit_level="4", lecturer_id=2))

def create_marks(db: Session) -> None:
    mark_repository = MarkRepository(db)

    mark_repository.add(Marks(mark="70", class_id="1", student_id=1))
    mark_repository.add(Marks(mark="54", class_id="2", student_id=1))
    mark_repository.add(Marks(mark="30", class_id="3", student_id=1))
    
    mark_repository.add(Marks(mark="61", class_id="1", student_id=2))
    mark_repository.add(Marks(mark="79", class_id="2", student_id=2))
    mark_repository.add(Marks(mark="55", class_id="3", student_id=2))
    
    mark_repository.add(Marks(mark="61", class_id="1", student_id=3))
    mark_repository.add(Marks(mark="89", class_id="2", student_id=3))
    mark_repository.add(Marks(mark="90", class_id="4", student_id=3))

def create_personal_circumstances(db: Session) -> None:
    personal_circumstance_repository = PersonalCircumstanceRepository(db)

    personal_circumstance_repository.add(
        PersonalCircumstance(
            details="01/01/2023 to 03/31/2023: Struggled with online learning environment",
            semester="1",
            cat="1",
            comments="Consider extension for Coursework",
            student_reg_no="abc12345"
        )
    )

    personal_circumstance_repository.add(
        PersonalCircumstance(
            details="03/31/2023 to 05/29/2023: Health Issues",
            semester="1",
            cat="3",
            comments="Discount attempt as CS426",
            student_reg_no="abc12345",
        )
    )

    personal_circumstance_repository.add(
        PersonalCircumstance(
            details="03/31/2023 to 05/29/2024: Mental Health Issues",
            semester="2",
            cat="2",
            comments="Discount attempt as CS412",
            student_reg_no="abc54321",
        )
    )

def create_academic_misconducts(db: Session) -> None:
    academic_misconduct_repository = AcademicMisconductRepository(db)

    academic_misconduct_repository.add(
        AcademicMisconduct(
            date="2024-01-01",
            outcome="UPHELD",
            student_reg_no="abc12345",
            class_code="CS412",
        )
    )

    academic_misconduct_repository.add(
        AcademicMisconduct(
            date="2024-02-01",
            outcome="UNDER INVESTIGATION",
            student_reg_no="abc12345",
            class_code="CS407",
        )
    )

    academic_misconduct_repository.add(
        AcademicMisconduct(
            date="2023-07-07",
            outcome="UNDER INVESTIGATION",
            student_reg_no="abc33311",
            class_code="CS407",
        )
    )


def main():
    database_url = DevelopmentConfig.DATABASE_URL or TestingConfig.DATABASE_URL
    
    if database_url:
        engine = create_engine(database_url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        initialise_roles(db)
        create_degree(db)
        create_students(db)
        create_users(db)
        create_classes(db)
        create_marks(db)
        create_personal_circumstances(db)
        create_academic_misconducts(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
