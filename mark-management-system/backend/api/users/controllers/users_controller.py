from fastapi import Depends, APIRouter, HTTPException
from faker import Faker

from sqlalchemy.orm import Session

from api.database import get_db

from api.system.schemas import schemas

from api.users.repositories.user_repository import UserRepository

from api.users.use_cases.create_user_use_case import CreateUserUseCase
from api.users.use_cases.get_users_use_case import GetUsersUseCase

from api.users.errors.user_already_exists import UserAlreadyExists
from api.users.errors.users_not_found import UsersNotFound

from api.users.hashers.bcrypt_hasher import BCryptHasher


users = APIRouter()
faker = Faker()


@users.post("/users/", response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    bcrypt_hasher = BCryptHasher()

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
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)

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
def get_user(user_id: int, db: Session = Depends(get_db)):
    ...

@users.delete("/users/{user_id}", response_model=schemas.User)
def delete_user():
    ...
