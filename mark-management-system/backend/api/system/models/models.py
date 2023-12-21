from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    reg_no = Column(String, unique=True, index=True)
    email_address = Column(String, unique=True, index=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    personal_circumstances = Column(String)

    roles = relationship("Role", secondary="role_members", backref="users")
    classes = relationship("Class", back_populates="lecturer")

class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True)

    level = Column(String, nullable=False)
    name = Column(String, nullable=False)

    classes = relationship("Class", back_populates="degree")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

class RoleMembers(Base):
    __tablename__ = "role_members"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True, nullable=False)

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    credit = Column(Integer, nullable=False)

    lecturer_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    degree_id = Column(Integer, ForeignKey("degrees.id"), index=True, nullable=False)

    degree = relationship("Degree", back_populates="classes")
    lecturer = relationship("User", back_populates="classes")
    marks = relationship("Marks", back_populates="class_")

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)

    mark = Column(Integer, nullable=False)

    class_id = Column(Integer, ForeignKey("classes.id"), index=True)
    student_id = Column(Integer, ForeignKey("users.id"), index=True)

    class_ = relationship("Class", back_populates="marks")

class DegreeClass(Base):
    __tablename__ = "degree_class"

    id = Column(Integer, primary_key=True, index=True)

    degree_id = Column(Integer, ForeignKey("degrees.id"), primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), primary_key=True, index=True)
