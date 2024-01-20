from fastapi import Depends

from sqlalchemy.orm import Session

from api.database import get_db

from api.users.repositories.user_repository import UserRepository

from api.users.hashers.bcrypt_hasher import BCryptHasher

from api.users.use_cases.create_user_use_case import CreateUserUseCase
from api.users.use_cases.login_user_use_case import LoginUserUseCase
from api.users.use_cases.get_users_use_case import GetUsersUseCase
from api.users.use_cases.get_user_use_case import GetUserUseCase

from api.users.validators import EmailAddressValidator
from api.users.validators import PasswordValidator

from api.config import Config



def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_bcrypt_hasher() -> BCryptHasher:
    return BCryptHasher()

def get_email_address_validator() -> EmailAddressValidator:
    return EmailAddressValidator()

def get_password_validator() -> PasswordValidator:
    return PasswordValidator()

def create_user_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
        bcrypt_hasher: BCryptHasher = Depends(get_bcrypt_hasher)
    ) -> CreateUserUseCase:
    return CreateUserUseCase(
        user_repository, 
        bcrypt_hasher
    )

def login_user_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
        bcrypt_hasher: BCryptHasher = Depends(get_bcrypt_hasher),
        config: Config = Depends(Config)
    ) -> LoginUserUseCase:
    return LoginUserUseCase(
        user_repository, 
        bcrypt_hasher,
        config
    )

def get_user_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> GetUserUseCase:
    return GetUserUseCase(user_repository)

def get_users_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> GetUsersUseCase:
    return GetUsersUseCase(user_repository)
