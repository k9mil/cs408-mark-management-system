from fastapi import Depends, APIRouter, HTTPException
from faker import Faker

from api.system.schemas import schemas

from api.users.repositories.user_repository import UserRepository

from api.users.use_cases.create_user_use_case import CreateUserUseCase
from api.users.use_cases.get_users_use_case import GetUsersUseCase
from api.users.use_cases.get_user_use_case import GetUserUseCase

from api.users.errors.user_already_exists import UserAlreadyExists
from api.users.errors.users_not_found import UsersNotFound
from api.users.errors.user_not_found import UserNotFound

from api.users.hashers.bcrypt_hasher import BCryptHasher

from api.users.dependencies import get_user_repository

from api.users.validators import EmailAddressValidator, PasswordValidator


users = APIRouter()
faker = Faker()


@users.post("/users/", response_model=schemas.User)
def create_user(
    request: schemas.UserCreate,
    user_repository: UserRepository = Depends(get_user_repository)
):
    bcrypt_hasher = BCryptHasher()

    email_address_validator = EmailAddressValidator()
    password_validator = PasswordValidator()

    validation_email_errors = email_address_validator.validate_user_email_address(request.email_address)
    validation_password_errors = password_validator.validate_user_password(request.password)

    if validation_email_errors or validation_password_errors:
        raise HTTPException(
            status_code=400,
            detail={
                "email_errors": validation_email_errors,
                "password_errors": validation_password_errors
            }
        )

    create_user_use_case = CreateUserUseCase(
        user_repository,
        bcrypt_hasher,
        faker
    )

    try:
        return create_user_use_case.execute(request)
    except UserAlreadyExists as e:
        raise UserAlreadyExists(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/users/", response_model=list[schemas.User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    user_repository: UserRepository = Depends(get_user_repository)
):
    get_users_use_case = GetUsersUseCase(
        user_repository
    )

    try:
        return get_users_use_case.execute(skip, limit)
    except UsersNotFound as e:
        raise UsersNotFound(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/users/{user_id}", response_model=schemas.User)
def get_user(
    user_id: int,
    user_repository: UserRepository = Depends(get_user_repository)
):
    get_user_use_case = GetUserUseCase(
        user_repository
    )

    try:
        return get_user_use_case.execute(user_id)
    except UserNotFound as e:
        raise UsersNotFound(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
