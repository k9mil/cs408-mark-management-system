import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import Depends
from fastapi.testclient import TestClient

from api.users.dependencies import get_user_repository
from api.users.dependencies import get_bcrypt_hasher
from api.users.dependencies import get_email_address_validator
from api.users.dependencies import get_password_validator

from api.users.dependencies import get_create_user_use_case
from api.users.dependencies import get_users_use_case
from api.users.dependencies import get_user_use_case

from api.users.errors.user_already_exists import UserAlreadyExists
from api.users.errors.users_not_found import UsersNotFound
from api.users.errors.user_not_found import UserNotFound

from api import create_app


app = create_app()
client = TestClient(app)

class MockBCryptHasher:
    def hash(self, password: str):
        pass

    def check(self, hashed_password: str, password: str):
        pass

class MockEmailAddressValidator:
    def __init__(self):
        pass

    def validate_email_address(self, email_address: str) -> None:
        return None

    def validate_user_email_address(self, email_address: str = None) -> dict:
        return {}
    
class MockPasswordValidator:
    def __init__(self):
        pass

    def validate_password(self, password: str) -> None:
        return None

    def validate_user_password(self, password: str) -> dict:
        return {}

class MockDatabase:
    def __init__(self):
        pass

    def add(self, _: object):
        pass

    def commit(self):
        pass

    def refresh(self):
        pass

    def query(self):
        pass


class MockUserRepository:
    def __init__(self, database: MockDatabase):
        self.database = database

    def add(self, class_: object):
        self.database.add(class_)

    def find_by_email(self, email_address: str):
        if email_address == "john@doe2.com":
            return {
                "id": 1,
                "email_address": email_address,
                "first_name": "John",
                "last_name": "Doe",
                "roles": [],
                "classes": [],
            }
        
        return None

    def get_users(self, skip: int, limit: int):
        if skip == 123:
            return None
        
        return [{
            "id": 1,
            "email_address": "john@doe2.com",
            "first_name": "John",
            "last_name": "Doe",
            "roles": [],
            "classes": [],
        }]

    def get_user(self, user_id: int):
        if user_id < 2:
            return {
                "id": user_id,
                "email_address": "john@doe2.com",
                "first_name": "John",
                "last_name": "Doe",
                "roles": [],
                "classes": [],
            }
        
        return None

class MockCreateUserUseCase:
    def __init__(self, user_repository: MockUserRepository):
        self.user_repository = user_repository

    def execute(self, request: object):
        if self.user_repository.find_by_email(request.email_address):
            raise UserAlreadyExists("User already exists")

        return {
            "id": 1,
            "email_address": request.email_address,
            "first_name": "John",
            "last_name": "Doe",
            "roles": [],
            "classes": [],
        }
    
class MockGetUsersUseCase:
    def __init__(self, user_repository: MockUserRepository):
        self.user_repository = user_repository

    def execute(self, skip: int, limit: int):
        users = self.user_repository.get_users(skip, limit)

        if users is None:
             raise UsersNotFound("Users not found")

        return users
    
class MockGetUserUseCase:
    def __init__(self, user_repository: MockUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int):
        user = self.user_repository.get_user(user_id)

        if user is None:
             raise UserNotFound("User not found")

        return user

def override_database_dependency():
    return MockDatabase()

def override_user_repository_dependency(db = Depends(override_database_dependency)):
    return MockUserRepository(db)

def override_bcrypt_hasher_dependency():
    return MockCreateUserUseCase()

def override_email_adress_validator_dependency():
    return MockEmailAddressValidator()

def override_password_validator_dependency():
    return MockPasswordValidator()

def override_create_user_use_case_dependency(user_repository = Depends(override_user_repository_dependency)):
    return MockCreateUserUseCase(user_repository)

def override_get_users_use_case_dependency(user_repository = Depends(override_user_repository_dependency)):
    return MockGetUsersUseCase(user_repository)

def override_get_user_use_case_dependency(user_repository = Depends(override_user_repository_dependency)):
    return MockGetUserUseCase(user_repository)

app.dependency_overrides[get_user_repository] = override_user_repository_dependency
app.dependency_overrides[get_bcrypt_hasher] = override_bcrypt_hasher_dependency
app.dependency_overrides[get_email_address_validator] = override_email_adress_validator_dependency
app.dependency_overrides[get_password_validator] = override_password_validator_dependency
app.dependency_overrides[get_create_user_use_case] = override_create_user_use_case_dependency
app.dependency_overrides[get_users_use_case] = override_get_users_use_case_dependency
app.dependency_overrides[get_user_use_case] = override_get_user_use_case_dependency


def test_given_valid_user_request_when_create_user_is_called_then_status_code_is_200():
    SAMPLE_USER_DATA = {
        "email_address": "john@doe1.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "strathclyde123",
    }

    SAMPLE_RESPONSE_OBJECT = {
        "id": 1,
        "email_address": "john@doe1.com",
        "first_name": "John",
        "last_name": "Doe",
        "roles": [],
        "classes": [],
    }

    response = client.post(
        "/users/",
        json=SAMPLE_USER_DATA,
    )

    assert response.status_code == 200
    assert response.json() == SAMPLE_RESPONSE_OBJECT

def test_given_invalid_user_request_when_create_user_is_called_then_status_code_is_422():
    SAMPLE_USER_DATA = {
        "first_name": "John",
        "last_name": "Doe",
    }

    response = client.post(
        "/users/",
        json=SAMPLE_USER_DATA,
    )

    assert response.status_code == 422

def test_given_valid_user_request_but_user_exists_when_create_user_is_called_then_status_code_is_409():
    SAMPLE_USER_DATA = {
        "email_address": "john@doe2.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "strathclyde123",
    }

    response = client.post(
        "/users/",
        json=SAMPLE_USER_DATA,
    )

    assert response.status_code == 409

def test_given_valid_parameters_when_get_users_is_called_then_status_code_is_200():
    SAMPLE_SKIP = 1
    SAMPLE_LIMIT = 1

    SAMPLE_RESPONSE_OBJECT = [{
        "id": 1,
        "email_address": "john@doe2.com",
        "first_name": "John",
        "last_name": "Doe",
        "roles": [],
        "classes": [],
    }]

    response = client.get(
        "/users/",
        params={
            "skip": SAMPLE_SKIP, 
            "limit": SAMPLE_LIMIT,
        },
    )

    assert response.status_code == 200
    assert response.json() == SAMPLE_RESPONSE_OBJECT

def test_given_invalid_parameters_when_get_users_is_called_then_status_code_is_422():
    SAMPLE_SKIP = "skip"
    SAMPLE_LIMIT = "limit"

    response = client.get(
        "/users/",
        params={
            "skip": SAMPLE_SKIP, 
            "limit": SAMPLE_LIMIT,
        },
    )

    assert response.status_code == 422

def test_given_valid_parameters_but_users_not_found_when_get_users_is_called_then_status_code_is_409():
    SAMPLE_SKIP = 123
    SAMPLE_LIMIT = 1

    response = client.get(
        "/users/",
        params={
            "skip": SAMPLE_SKIP, 
            "limit": SAMPLE_LIMIT,
        },
    )

    assert response.status_code == 409

def test_given_valid_and_existing_user_id_when_get_user_is_called_then_status_code_is_200():
    SAMPLE_USER_ID = 1

    SAMPLE_RESPONSE_OBJECT = {
        "id": 1,
        "email_address": "john@doe2.com",
        "first_name": "John",
        "last_name": "Doe",
        "roles": [],
        "classes": [],
    }

    response = client.get(
        f"/users/{SAMPLE_USER_ID}",
    )

    assert response.status_code == 200
    assert response.json() == SAMPLE_RESPONSE_OBJECT

def test_given_invalid_user_id_when_get_user_is_called_then_status_code_is_422():
    SAMPLE_USER_ID = "france"

    response = client.get(
        f"/users/{SAMPLE_USER_ID}",
    )

    assert response.status_code == 422

def test_given_valid_user_id_but_no_user_when_get_user_is_called_then_status_code_is_409():
    SAMPLE_USER_ID = 2

    response = client.get(
        f"/users/{SAMPLE_USER_ID}",
    )

    assert response.status_code == 409