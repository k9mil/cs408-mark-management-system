from fastapi import Depends

from sqlalchemy.orm import Session

from api.database import get_db

from api.classes.repositories.class_repository import ClassRepository
from api.users.repositories.user_repository import UserRepository

from api.classes.use_cases.create_class_use_case import CreateClassUseCase


def get_class_repository(db: Session = Depends(get_db)) -> ClassRepository:
    return ClassRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def create_class_use_case(
        class_repository: ClassRepository = Depends(get_class_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> CreateClassUseCase:
    return CreateClassUseCase(
        class_repository, 
        user_repository
    )
