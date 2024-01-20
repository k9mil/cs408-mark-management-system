from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Optional

from jose import jwt, JWTError

from api.config import Config


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)

def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    if not token:
        return None

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user_with_roles(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    if not token:
        return None

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return (payload.get("sub"), payload.get("is_admin"))
    except JWTError:
        return None
