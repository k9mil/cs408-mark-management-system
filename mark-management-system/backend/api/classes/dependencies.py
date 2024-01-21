from fastapi import Depends

from api.middleware.dependencies import ClassRepository
from api.middleware.dependencies import UserRepository

from api.classes.use_cases.create_class_use_case import CreateClassUseCase
from api.classes.use_cases.get_classes_use_case import GetClassesUseCase
from api.classes.use_cases.get_classes_for_lecturer_use_case import GetClassesForLecturerUseCase
from api.classes.use_cases.edit_class_use_case import EditClassUseCase
from api.classes.use_cases.delete_class_use_case import DeleteClassUseCase
from api.classes.use_cases.check_user_identity_use_case import CheckUserIdentityUseCase

from api.middleware.dependencies import get_class_repository
from api.middleware.dependencies import get_user_repository


def create_class_use_case(
        class_repository: ClassRepository = Depends(get_class_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> CreateClassUseCase:
    return CreateClassUseCase(
        class_repository, 
        user_repository
    )

def get_classes_use_case(
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> GetClassesUseCase:
    return GetClassesUseCase(
        class_repository, 
    )

def get_classes_for_lecturer_use_case(
        class_repository: ClassRepository = Depends(get_class_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> GetClassesForLecturerUseCase:
    return GetClassesForLecturerUseCase(
        class_repository, 
        user_repository
    )

def edit_class_use_case(
        class_repository: ClassRepository = Depends(get_class_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> EditClassUseCase:
    return EditClassUseCase(
        class_repository, 
        user_repository
    )

def delete_class_use_case(
        class_repository: ClassRepository = Depends(get_class_repository),
    ) -> DeleteClassUseCase:
    return DeleteClassUseCase(
        class_repository, 
    )

def check_user_identity_use_case(
        class_repository: ClassRepository = Depends(get_class_repository),
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> CheckUserIdentityUseCase:
    return CheckUserIdentityUseCase(
        class_repository, 
        user_repository
    )
