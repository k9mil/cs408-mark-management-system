from fastapi import Depends

from api.middleware.dependencies import UserRepository
from api.middleware.dependencies import ClassRepository
from api.middleware.dependencies import MarkRepository

from api.users.hashers.bcrypt_hasher import BCryptHasher

from api.users.use_cases.create_user_use_case import CreateUserUseCase
from api.users.use_cases.login_user_use_case import LoginUserUseCase
from api.users.use_cases.get_users_use_case import GetUsersUseCase
from api.users.use_cases.get_user_use_case import GetUserUseCase
from api.users.use_cases.get_lecturers_use_case import GetLecturersUseCase
from api.users.use_cases.get_lecturer_use_case import GetLecturerUseCase
from api.users.use_cases.edit_user_use_case import EditUserUseCase

from api.users.validators import EmailAddressValidator
from api.users.validators import PasswordValidator

from api.config import Config

from api.middleware.dependencies import get_user_repository
from api.middleware.dependencies import get_class_repository
from api.middleware.dependencies import get_mark_repository


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

def get_lecturers_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
        mark_repository: MarkRepository = Depends(get_mark_repository),
    ) -> GetLecturersUseCase:
    return GetLecturersUseCase(
        user_repository, 
        class_repository,
        mark_repository,
    )

def get_lecturer_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
        class_repository: ClassRepository = Depends(get_class_repository),
        mark_repository: MarkRepository = Depends(get_mark_repository),
    ) -> GetLecturerUseCase:
    return GetLecturerUseCase(
        user_repository, 
        class_repository,
        mark_repository,
    )

def edit_user_use_case(
        user_repository: UserRepository = Depends(get_user_repository),
        bcrypt_hasher: BCryptHasher = Depends(get_bcrypt_hasher),
    ) -> EditUserUseCase:
    return EditUserUseCase(
        user_repository, 
        bcrypt_hasher,
    )

def get_user_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> GetUserUseCase:
    return GetUserUseCase(user_repository)

def get_users_use_case(user_repository: UserRepository = Depends(get_user_repository)) -> GetUsersUseCase:
    return GetUsersUseCase(user_repository)
