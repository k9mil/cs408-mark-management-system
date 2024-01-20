from fastapi.security import OAuth2PasswordRequestForm

from typing import List
from jose import jwt
from datetime import datetime, timedelta

from api.system.schemas.schemas import UserDetails

from api.users.repositories.user_repository import UserRepository

from api.users.errors.user_not_found import UserNotFound
from api.users.errors.invalid_credentials import InvalidCredentials

from api.users.hashers.bcrypt_hasher import BCryptHasher

from api.config import Config


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, bcrypt_hasher: BCryptHasher, config: Config):
        self.user_repository = user_repository
        self.bcrypt_hasher = bcrypt_hasher
        self.config = config
    
    def execute(self, form_data: OAuth2PasswordRequestForm) -> UserDetails:
        user = self.user_repository.find_by_email(form_data.username)

        if user is None:
            raise UserNotFound("User not found")
        
        if not self.bcrypt_hasher.check(user.password, form_data.password):
            raise InvalidCredentials("Invalid Credentials provided")

        access_token = self.create_access_token(user.email_address, user.roles)
        refresh_token = self.create_refresh_token(user.email_address)

        user_details = UserDetails(
            access_token=access_token,
            refresh_token=refresh_token,
            email_address=user.email_address,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        return user_details

    def create_access_token(self, subject: str, roles: List[str]):
        expire = datetime.utcnow() + timedelta(minutes=self.config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        is_admin = any(role.title == "admin" for role in roles)
        is_lecturer = any(role.title == "lecturer" for role in roles)

        to_encode = ({"exp": expire, "sub": str(subject), "is_admin": is_admin, "is_lecturer": is_lecturer})
        encoded_jwt = jwt.encode(to_encode, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)

        return encoded_jwt
    
    def create_refresh_token(self, subject: str) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=self.config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.config.JWT_REFRESH_SECRET_KEY, self.config.JWT_ALGORITHM)
        
        return encoded_jwt
