from pydantic import BaseModel

from typing import List


class RoleBase(BaseModel):
    title: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email_address: str
    first_name: str
    last_name: str
    personal_circumstances: str | None = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    reg_no: str
    roles: List[Role] = []

    class Config:
        orm_mode = True


class DegreeBase(BaseModel):
    level: str
    name: str

class DegreeCreate(DegreeBase):
    pass

class Degree(DegreeBase):
    id: int
    classes: List["Class"] = []

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


class ClassBase(BaseModel):
    name: str
    code: str
    credit: int

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int

    lecturer: User
    
    marks: List["Marks"] = []
    degrees: List[Degree] = []

    class Config:
        orm_mode = True


class MarksBase(BaseModel):
    mark: int
    class_id: int
    student_id: int

class MarksCreate(MarksBase):
    pass

class Marks(MarksBase):
    id: int

    class_id: int
    student_id: int

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
