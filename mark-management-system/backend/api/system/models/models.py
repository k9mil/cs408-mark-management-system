from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    email_address = Column(String(256), unique=True, index=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    password = Column(String(256), nullable=False)

    classes = relationship("Class", back_populates="lecturer")
    roles = relationship("Role", secondary="role_users", back_populates="users")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    reg_no = Column(String(256), unique=True, index=True)
    student_name = Column(String(128), nullable=False)

    degree_id = Column(Integer, ForeignKey("degrees.id"), index=True, nullable=False)

    degree = relationship("Degree", back_populates="students")
    personal_circumstances = relationship("PersonalCircumstance", back_populates="student")

    classes = relationship("Class", secondary="marks", back_populates="students")

class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    level = Column(String(64), nullable=False)
    name = Column(String(256), nullable=False)

    students = relationship("Student", back_populates="degree")
    classes = relationship("Class", secondary="degree_classes", back_populates="degrees")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(64), nullable=False)

    users = relationship("User", secondary="role_users", back_populates="roles")

class RoleUsers(Base):
    __tablename__ = "role_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    name = Column(String(128), nullable=False)
    code = Column(String(32), nullable=False)
    credit = Column(Integer, nullable=False)
    credit_level = Column(Integer, nullable=False)

    lecturer_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    lecturer = relationship("User", back_populates="classes")
    students = relationship("Student", secondary="marks", back_populates="classes")
    degrees = relationship("Degree", secondary="degree_classes", back_populates="classes")

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    mark = Column(Integer, nullable=False)

    class_id = Column(Integer, ForeignKey("classes.id"), index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)

class DegreeClasses(Base):
    __tablename__ = "degree_classes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    degree_id = Column(Integer, ForeignKey("degrees.id"), primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), primary_key=True, nullable=False)

class PersonalCircumstance(Base):
    __tablename__ = "personal_circumstances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    details = Column(String(512), nullable=False)
    semester = Column(String(8), nullable=False)
    cat = Column(Integer, nullable=False)
    comments = Column(String(256), nullable=False)

    students = Column(Integer, ForeignKey("students.id"), index=True)

    student = relationship("Student", back_populates="personal_circumstances")
