from pydantic import BaseModel

from typing import List, Optional, ForwardRef

from datetime import date


Class = ForwardRef("Class")
Student = ForwardRef("Student")
Marks = ForwardRef("Marks")
User = ForwardRef("User")
Degree = ForwardRef("Degree")


class RoleBase(BaseModel):
    title: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    users: List["User"] = []

    class Config:   
        from_attributes = True

class RoleInUser(RoleBase):
    id: int

class MarksBase(BaseModel):
    mark: int | None = None
    code: str | None = None

    class_id: int
    student_id: int

class MarksCreate(MarksBase):
    pass

class MarksEdit(BaseModel):
    id: int
    
    mark: int | None = None
    code: str | None = None

class MarksRow(BaseModel):
    id: int

    class_code: str
    class_name: str | None
    reg_no: str
    mark: int | None = None
    code: str | None = None
    student_name: str
    degree_level: str
    degree_name: str

class Marks(MarksBase):
    id: int

    class Config:
        from_attributes = True

class MarksStatistics(BaseModel):
    mean: int
    median: int
    mode: int
    pass_rate: int

    first_bucket: int | None
    second_bucket: int | None
    third_bucket: int | None
    fourth_bucket: int | None
    fifth_bucket: int | None

class DegreeBase(BaseModel):
    level: str
    name: str
    code: str

class DegreeCreate(DegreeBase):
    pass

class Degree(DegreeBase):
    id: int

    students: List["StudentBase"] = []
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

class UserEdit(BaseModel):
    id: int
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    password: Optional[str] = None
    confirm_password: Optional[str] = None

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

class ClassBaseMetric(ClassBase):
    mean: int
    stdev: float

class ClassCreate(ClassBase):
    lecturer_id: int

class ClassEdit(ClassBase):
    id: int

    original_code: str
    lecturer_id: int

class Class(ClassBase):
    id: int
    
    lecturer: UserBase # type: ignore
    students: List["StudentBase"] = [] # type: ignore
    marks: List[Marks] = []

    class Config:
        from_attributes = True

class MarksMetrics(BaseModel):
    lowest_performing_classes: List[ClassBaseMetric]
    highest_performing_classes: List[ClassBaseMetric]
    most_consistent_classes: List[ClassBaseMetric]

class LecturerClass(ClassBase):
    is_uploaded: bool

class Lecturer(BaseModel):
    id: int
    
    first_name: str
    last_name: str
    number_of_classes_taught: int
    
    classes: List["LecturerClass"] = []

class AcademicMisconductBase(BaseModel):
    date: date
    outcome: str
    
class AcademicMisconductCreate(AcademicMisconductBase):
    reg_no: str
    class_code: str

class AcademicMisconduct(AcademicMisconductBase):
    id: int

    class Config:
        orm_mode = True


class ClassWithMisconduct(ClassBase):
    academic_misconducts: List[AcademicMisconductCreate] | None

class PersonalCircumstancesBase(BaseModel):
    details: str
    semester: str
    cat: int
    comments: str

class PersonalCircumstancesCreate(PersonalCircumstancesBase):
    reg_no: str

class PersonalCircumstances(PersonalCircumstancesBase):
    id: int

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    reg_no: str
    student_name: str
    year: int

    degree_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    degree: DegreeBase
    classes: List[ClassWithMisconduct] = []
    personal_circumstances: List[PersonalCircumstancesBase] = []

    class Config:
        from_attributes = True

class StudentStatistics(BaseModel):
    mean: int
    max_mark: int
    min_mark: int
    pass_rate: int


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
    id: int
    
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
