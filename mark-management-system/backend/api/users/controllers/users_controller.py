from fastapi import Depends, APIRouter, HTTPException

from api.system.schemas import schemas

from api.users.use_cases.create_user_use_case import CreateUserUseCase
from api.users.use_cases.get_users_use_case import GetUsersUseCase
from api.users.use_cases.get_user_use_case import GetUserUseCase

from api.users.errors.user_already_exists import UserAlreadyExists
from api.users.errors.users_not_found import UsersNotFound
from api.users.errors.user_not_found import UserNotFound

from api.users.dependencies import get_email_address_validator
from api.users.dependencies import get_password_validator

from api.users.dependencies import create_user_use_case
from api.users.dependencies import get_users_use_case
from api.users.dependencies import get_user_use_case

from api.users.validators import EmailAddressValidator
from api.users.validators import PasswordValidator


users = APIRouter()


@users.post("/users/", response_model=schemas.User)
def create_user(
    request: schemas.UserCreate,
    create_user_use_case: CreateUserUseCase = Depends(create_user_use_case),
    email_address_validator: EmailAddressValidator = Depends(get_email_address_validator),
    password_validator: PasswordValidator = Depends(get_password_validator)
):
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

    try:
        return create_user_use_case.execute(request)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/users/", response_model=list[schemas.User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    get_users_use_case: GetUsersUseCase = Depends(get_users_use_case),
):
    try:
        return get_users_use_case.execute(skip, limit)
    except UsersNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/users/{user_id}", response_model=schemas.User)
def get_user(
    user_id: int,
    get_user_use_case: GetUserUseCase = Depends(get_user_use_case),
):
    try:
        return get_user_use_case.execute(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
