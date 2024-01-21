from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from typing import Optional

from jose import jwt, JWTError

from api.database import get_db

from api.users.repositories.user_repository import UserRepository
from api.roles.repositories.roles_repository import RolesRepository
from api.classes.repositories.class_repository import ClassRepository

from api.config import Config


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)


def get_roles_repository(db: Session = Depends(get_db)) -> RolesRepository:
    print(f"Session ID in endpoint (roles): {hash(db)}")
    return RolesRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    print(f"Session ID in endpoint (user): {hash(db)}")
    return UserRepository(db)

def get_class_repository(db: Session = Depends(get_db)) -> ClassRepository:
    print(f"Session ID in endpoint (class): {hash(db)}")
    return ClassRepository(db)


def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    if not token:
        return None

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return (payload.get("sub"), payload.get("is_admin"))
    except JWTError:
        return None