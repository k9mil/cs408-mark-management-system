from fastapi import Depends, APIRouter
from faker import Faker

from sqlalchemy.orm import Session

from api.database import get_db

from api.system.schemas import schemas

from api.users.repositories.user_repository import UserRepository

from api.users.use_cases.create_user_use_case import CreateUserUseCase

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

    return create_user_use_case.execute(request)

@users.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ...

@users.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    ...

@users.delete("/users/{user_id}", response_model=schemas.User)
def delete_user():
    ...
