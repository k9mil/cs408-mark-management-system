from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    reg_no = Column(Integer, unique=True, index=True)
    email_address = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    personal_circumstances = Column(String)

    roles = relationship("Role", secondary="role_members", back_populates="users")

class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True)

    level = Column(String)
    name = Column(String)

    classes = relationship("Class", back_populates="degree")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

class RoleMembers(Base):
    __tablename__ = "role_members"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String)
    code = Column(String)
    credit = Column(Integer)

    lecturer = relationship("User", back_populates="class")
    marks = relationship("Marks", back_populates="class")

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)

    mark = Column(Integer)

    class_id = Column(Integer, ForeignKey("classes.id"), index=True)
    student_id = Column(Integer, ForeignKey("users.id"), index=True)

class DegreeClass(Base):
    __tablename__ = "degree_class"

    id = Column(Integer, primary_key=True, index=True)

    degree_id = Column(Integer, ForeignKey("degrees.id"), primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), primary_key=True, index=True)
