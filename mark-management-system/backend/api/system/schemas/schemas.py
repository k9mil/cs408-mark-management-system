from pydantic import BaseModel

from typing import List, ForwardRef


Class = ForwardRef('Class')
Student = ForwardRef('Student')
Marks = ForwardRef('Marks')
User = ForwardRef('User')
Degree = ForwardRef('Degree')


class RoleBase(BaseModel):
    title: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    # TODO: fix circular dependency via ForwardRef
    users: List["User"] = []

    class Config:   
        from_attributes = True

class RoleInUser(RoleBase):
    id: int

class MarksBase(BaseModel):
    mark: int

    class_id: int
    student_id: int
    unique_code: str

class MarksCreate(MarksBase):
    pass

class Marks(MarksBase):
    id: int

    class Config:
        from_attributes = True


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
        from_attributes = True

class DegreeClassBase(BaseModel):
    pass

class DegreeClassCreate(DegreeClassBase):
    degree_id: int
    class_id: int

class DegreeClass(DegreeClassBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email_address: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email_address: str
    password: str

class User(UserBase):
    id: int
    
    roles: List[RoleInUser] = []
    classes: List["Class"] = [] # type: ignore

    class Config:
        from_attributes = True

class ClassBase(BaseModel):
    name: str
    code: str
    credit: int
    credit_level: int

class ClassCreate(ClassBase):
    lecturer_id: int

class ClassEdit(ClassBase):
    id: int
    
    lecturer_id: int

class Class(ClassBase):
    id: int
    
    lecturer: UserBase # type: ignore
    students: List["Student"] = [] # type: ignore
    marks: List[Marks] = []

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    reg_no: str
    student_name: str
    personal_circumstances: str | None = None

    degree_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    degree: DegreeBase
    classes: List[ClassBase] = []

    class Config:
        from_attributes = True


class RoleUsersBase(BaseModel):
    pass

class RoleUsersData(RoleUsersBase):
    role_id: int
    user_id: int

class RoleUsers(RoleUsersData):
    id: int

    class Config:
        from_attributes = True

class UserDetails(UserBase):
    access_token: str
    refresh_token: str
    
    roles: List[RoleInUser] = []
    classes: List[Class] = [] # type: ignore

    class Config:
        from_attributes = True

User.model_rebuild()
Class.model_rebuild()
Student.model_rebuild()
Marks.model_rebuild()
Degree.model_rebuild()
