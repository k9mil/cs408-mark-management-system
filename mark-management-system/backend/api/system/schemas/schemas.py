from pydantic import BaseModel

from typing import List


class RoleBase(BaseModel):
    title: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    # TODO: fix circular dependency via ForwardRef
    users: List["User"] = []

    class Config:   
        orm_mode = True

class MarksBase(BaseModel):
    mark: int

    class_id: int
    student_id: int
    unique_code: str

class MarksCreate(MarksBase):
    pass

class Marks(MarksBase):
    id: int

    # TODO: fix circular dependency via ForwardRef
    classes: List["Class"] = []

    class Config:
        orm_mode = True


class DegreeBase(BaseModel):
    level: str
    name: str

class DegreeCreate(DegreeBase):
    pass

class Degree(DegreeBase):
    id: int

    # TODO: fix circular dependency via ForwardRef
    students: List["Student"] = []
    classes: List["Class"] = []

    class Config:
        orm_mode = True

class DegreeClassBase(BaseModel):
    pass

class DegreeClassCreate(DegreeClassBase):
    degree_id: int
    class_id: int

class DegreeClass(DegreeClassBase):
    id: int

    class Config:
        orm_mode = True

class ClassBase(BaseModel):
    name: str
    code: str
    credit: int
    credit_level: int

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int

    # TODO: fix circular dependency via ForwardRef
    lecturer: "User" # type: ignore
    
    students: List["Student"] = [] # type: ignore
    marks: List[Marks] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email_address: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    roles: List[Role] = []
    classes: List[Class] = []

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    reg_no: str
    student_name: str
    personal_circumstances: str | None = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    degree_id: int

    degree: Degree
    classes: List[Class] = []

    class Config:
        orm_mode = True


class RoleMembersBase(BaseModel):
    pass

class RoleMembersCreate(RoleMembersBase):
    role_id: int
    user_id: int

class RoleMembers(RoleMembersBase):
    id: int

    class Config:
        orm_mode = True
