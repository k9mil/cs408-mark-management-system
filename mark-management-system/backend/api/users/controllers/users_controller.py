from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Tuple, List

from api.system.schemas import schemas

from api.users.use_cases.create_user_use_case import CreateUserUseCase
from api.users.use_cases.login_user_use_case import LoginUserUseCase
from api.users.use_cases.get_users_use_case import GetUsersUseCase
from api.users.use_cases.get_user_use_case import GetUserUseCase
from api.users.use_cases.get_lecturers_use_case import GetLecturersUseCase
from api.users.use_cases.get_lecturer_use_case import GetLecturerUseCase
from api.users.use_cases.edit_user_use_case import EditUserUseCase

from api.users.errors.user_already_exists import UserAlreadyExists
from api.users.errors.users_not_found import UsersNotFound
from api.users.errors.user_not_found import UserNotFound
from api.users.errors.invalid_credentials import InvalidCredentials
from api.users.errors.lecturers_not_found import LecturersNotFound

from api.users.dependencies import get_email_address_validator
from api.users.dependencies import get_password_validator

from api.users.dependencies import create_user_use_case
from api.users.dependencies import login_user_use_case
from api.users.dependencies import get_users_use_case
from api.users.dependencies import get_user_use_case
from api.users.dependencies import get_lecturers_use_case
from api.users.dependencies import get_lecturer_use_case
from api.users.dependencies import edit_user_use_case

from api.middleware.dependencies import get_current_user

from api.users.validators import EmailAddressValidator
from api.users.validators import PasswordValidator


users = APIRouter()


@users.post("/api/v1/users", response_model=schemas.User)
def create_user(
    request: schemas.UserCreate,
    create_user_use_case: CreateUserUseCase = Depends(create_user_use_case),
    email_address_validator: EmailAddressValidator = Depends(get_email_address_validator),
    password_validator: PasswordValidator = Depends(get_password_validator)
):
    """
    Create a new user in the system.    
    
    **Note**: This feature is endpoint-only for now, no frontend exists for it.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:    
        - `request`: A `schemas.UserCreate` object is required which contains the necessary user details for user creation.  
        - `create_user_use_case`: The class which handles the business logic for user creation.   
        - `email_address_validator`: A validator class which ensures that the e-mail addrses is valid.  
        - `password_validator`: A validator class which ensures that the password is valid.  

    Raises:  
        - `HTTPException`, 400: If the e-mail, or password validation fails.  
        - `HTTPException`, 409: If the user already exists in the system.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.User` schema, which contains the details of the created user.  
    """
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
    
@users.post("/api/v1/users/login", response_model=schemas.UserDetails)
def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_user_use_case: LoginUserUseCase = Depends(login_user_use_case),
):
    """
    Authenticates the user in order to create & provide a JWT.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `form_data`: The data from the form which will be authenticated against the database.  
        - `login_user_use_case`: The class which handles the business logic for authentication.   

    Raises:  
        - `HTTPException`, 401: If the credentials provided in the form are invalid.  
        - `HTTPException`, 404: If the user cannot be found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.UserDetails` schema, which contains mostly data with regards to authentication, i.e. a JWT token and a refresh token.  
    """
    try:
        return login_user_use_case.execute(form_data)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidCredentials as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/api/v1/users", response_model=List[schemas.User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_users_use_case: GetUsersUseCase = Depends(get_users_use_case),
):
    """
    Retrieves a list of users in the system.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `skip` (default: 0): A parameter which determines how many objects to skip.  
        - `limit` (default: 100): A parameter which determines the maximum amount of users to return.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_users_use_case`: The class which handles the business logic for user retrieval.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If no users have been found and returned.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.User]` schema, which returns a list of Users.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_users_use_case.execute(skip, limit, current_user)
    except UsersNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/api/v1/users/{user_id}", response_model=schemas.User)
def get_user(
    user_id: int,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_user_use_case: GetUserUseCase = Depends(get_user_use_case),
):
    """
    Retrieves a particular user given a user_id.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `user_id`: The `user_id` of the user which is to be retrieved.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_user_use_case`: The class which handles the business logic for retrieving a user.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user has not been found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.User` schema, which returns the queried user.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )
    
    try:
        return get_user_use_case.execute(user_id, current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@users.put("/api/v1/users/{user_id}", response_model=schemas.User)
def edit_user(
    request: schemas.UserEdit,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    edit_user_use_case: EditUserUseCase = Depends(edit_user_use_case),
    password_validator: PasswordValidator = Depends(get_password_validator)
):
    """
    Allows for editing an already existing user.    

    **Note**: No email validator is present as the system does not fully support editing email addresses.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `request`: A `schemas.UserEdit` object is which contains all of the new fields to replace the existing details.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.  
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `edit_user_use_case`: The class which handles the business logic for editing the user details.  
        - `password_validator`: A validator class which ensures that the password is valid.  
        
    Raises:  
        - `HTTPException`, 400: If the e-mail, or password validation fails.  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user has not been found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.User` schema, which returns the details of the newly edited user.  
    """
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
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@users.get("/api/v1/lecturers", response_model=List[schemas.Lecturer])
def get_lecturers(
    skip: int = 0,
    limit: int = 100,
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_lecturers_use_case: GetLecturersUseCase = Depends(get_lecturers_use_case),
):
    """
    Retrieves a list of users with the lecturer role in the system.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `skip` (default: 0): A parameter which determines how many objects to skip.  
        - `limit` (default: 100): A parameter which determines the maximum amount of users to return.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_lecturers_use_case`: The class which handles the business logic for lecturer retrieval.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If no users have been found and returned.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `List[schemas.Lecturer]` schema, which returns a list of Lecturers.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_lecturers_use_case.execute(skip, limit, current_user)
    except LecturersNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@users.get("/api/v1/lecturers/{user_id}", response_model=schemas.Lecturer)
def get_lecturer(
    current_user: Tuple[str, bool, bool] = Depends(get_current_user),
    get_lecturer_use_case: GetLecturerUseCase = Depends(get_lecturer_use_case),
):
    """
    Retrieves a particular user (lecturer).    

    **Note**: No identifier is passed in, only the requestor can view the lecturer (their own) details, via JWT.    

    **Note**: If you are viewing the below documentation from OpenAPI, or Redocly API docs, be aware that the documentation is mainly concerning the code, and that there may be some differences.
    OpenAPI and Redocly API docs only show FastAPI (Pydantic) responses, i.e. 200 & 422, and ignore custom exceptions.

    Args:  
        - `user_id`: The `user_id` of the user. Not used, for RESTful purposes.  
        - `current_user`: A middleware object `current_user` which contains a Tuple of a string, boolean and a boolean.   
                      The initial string is the user_email (which is extracted from the JWT), followed by is_admin & is_lecturer flags.  
        - `get_user_use_case`: The class which handles the business logic for retrieving a user.  

    Raises:  
        - `HTTPException`, 401: If the `current_user` is None, i.e. if the JWT is invalid, missing or corrupt.  
        - `HTTPException`, 403: If there has been a permission error.  
        - `HTTPException`, 404: If the user has not been found.  
        - `HTTPException`, 500: If any other system exception occurs.  

    Returns:  
        - `response_model`: The response is in the model of the `schemas.User` schema, which returns the queried user.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid JWT provided",
        )

    try:
        return get_lecturer_use_case.execute(current_user)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
