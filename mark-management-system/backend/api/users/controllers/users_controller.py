from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Tuple, List

from api.system.schemas import schemas

from api.users.use_cases.create_user_use_case import CreateUserUseCase
from api.users.use_cases.login_user_use_case import LoginUserUseCase
from api.users.use_cases.get_users_use_case import GetUsersUseCase
from api.users.use_cases.get_user_use_case import GetUserUseCase
from api.users.use_cases.get_lecturers_use_case import GetLecturersUseCase
from api.users.use_cases.edit_user_use_case import EditUserUseCase

from api.users.errors.user_already_exists import UserAlreadyExists
from api.users.errors.users_not_found import UsersNotFound
from api.users.errors.user_not_found import UserNotFound
from api.users.errors.invalid_credentials import InvalidCredentials

from api.users.dependencies import get_email_address_validator
from api.users.dependencies import get_password_validator

from api.users.dependencies import create_user_use_case
from api.users.dependencies import login_user_use_case
from api.users.dependencies import get_users_use_case
from api.users.dependencies import get_user_use_case
from api.users.dependencies import get_lecturers_use_case
from api.users.dependencies import edit_user_use_case

from api.middleware.dependencies import get_current_user

from api.users.validators import EmailAddressValidator
from api.users.validators import PasswordValidator


users = APIRouter()


@users.post("/users/register", response_model=schemas.User)
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
    
@users.post("/users/login", response_model=schemas.UserDetails)
def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_user_use_case: LoginUserUseCase = Depends(login_user_use_case),
):
    try:
        return login_user_use_case.execute(form_data)
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidCredentials as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/users/", response_model=List[schemas.User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_users_use_case: GetUsersUseCase = Depends(get_users_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_users_use_case.execute(skip, limit, current_user)
    except UsersNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/users/lecturers/", response_model=List[schemas.Lecturer])
def get_lecturers(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_lecturers_use_case: GetLecturersUseCase = Depends(get_lecturers_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_lecturers_use_case.execute(skip, limit, current_user)
    except UsersNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/users/{user_id}", response_model=schemas.User)
def get_user(
    user_id: int,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    get_user_use_case: GetUserUseCase = Depends(get_user_use_case),
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )
    
    try:
        return get_user_use_case.execute(user_id, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@users.post("/users/{user_id}", response_model=schemas.User)
def edit_user(
    request: schemas.UserEdit,
    current_user: Tuple[str, bool] = Depends(get_current_user),
    edit_user_use_case: EditUserUseCase = Depends(edit_user_use_case),
    password_validator: PasswordValidator = Depends(get_password_validator)
):
    if request.password and request.confirm_password:
        validation_password_errors = password_validator.validate_user_password(request.password)
        validation_confirm_password_errors = password_validator.validate_user_password(request.confirm_password)

        if validation_password_errors or validation_confirm_password_errors:
            raise HTTPException(
                status_code=400,
                detail={
                    "password_errors": validation_password_errors,
                    "confirm_password_errors": validation_confirm_password_errors
                }
            )

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )
    
    try:
        return edit_user_use_case.execute(request, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
