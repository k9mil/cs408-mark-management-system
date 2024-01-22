from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from typing import Optional

from jose import jwt, JWTError

from api.database import get_db

from api.users.repositories.user_repository import UserRepository
from api.roles.repositories.roles_repository import RolesRepository
from api.classes.repositories.class_repository import ClassRepository
from api.students.repositories.student_repository import StudentRepository
from api.degrees.repositories.degree_repository import DegreeRepository
from api.marks.repositories.mark_repository import MarkRepository

from api.config import Config


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)


def get_roles_repository(db: Session = Depends(get_db)) -> RolesRepository:
    return RolesRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_class_repository(db: Session = Depends(get_db)) -> ClassRepository:
    return ClassRepository(db)

def get_student_repository(db: Session = Depends(get_db)) -> StudentRepository:
    return StudentRepository(db)

def get_degree_repository(db: Session = Depends(get_db)) -> DegreeRepository:
    return DegreeRepository(db)

def get_mark_repository(db: Session = Depends(get_db)) -> MarkRepository:
    return MarkRepository(db)


def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    if not token:
        return None

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return (payload.get("sub"), payload.get("is_admin"))
    except JWTError:
        return None
