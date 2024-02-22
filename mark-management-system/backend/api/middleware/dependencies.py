from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from typing import Optional, Tuple

from jose import jwt, JWTError

from api.database import get_db

from api.users.repositories.user_repository import UserRepository
from api.roles.repositories.roles_repository import RolesRepository
from api.classes.repositories.class_repository import ClassRepository
from api.students.repositories.student_repository import StudentRepository
from api.degrees.repositories.degree_repository import DegreeRepository
from api.marks.repositories.mark_repository import MarkRepository
from api.personal_circumstances.repositories.personal_circumstance_repostitory import PersonalCircumstanceRepository
from api.academic_misconducts.repositories.academic_misconduct_repository import AcademicMisconductRepository

from api.config import Config


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login",
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

def get_personal_circumstance_repository(db: Session = Depends(get_db)) -> PersonalCircumstanceRepository:
    return PersonalCircumstanceRepository(db)

def get_academic_misconduct_repository(db: Session = Depends(get_db)) -> AcademicMisconductRepository:
    return AcademicMisconductRepository(db)


def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[Tuple[str, bool, bool]]:
    """
    Serves as the primary middleware of the application. Retrieves a user's information given a JWT token.

    Args:
        token: The JWT token which the information is extracted from.

    Raises:
        JWTError: If the decoding fails, a JWTError is "raised", i.e. returns None.

    Returns:
        Optional[Tuple[str, bool, bool]]: Returns a Tuple containing user_email, an is_admin boolean flag and a is_lecturer boolean flag. 
                                          If a token isn't found, or if no secret key is found, or if decoding fails "None" is returned.
    """
    if not token:
        return None

    try:
        if Config.JWT_SECRET_KEY:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])

            if payload is not None:
                user_email = payload.get("sub")
                is_admin = payload.get("is_admin")
                is_lecturer = payload.get("is_lecturer")

                return (str(user_email), bool(is_admin), bool(is_lecturer))
        return None
    except JWTError:
        return None
