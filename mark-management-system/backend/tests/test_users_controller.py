import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import Depends
from fastapi.testclient import TestClient

from api.users.dependencies import get_user_repository
from api.users.dependencies import get_bcrypt_hasher
from api.users.dependencies import get_create_user_use_case
from api.users.dependencies import get_email_address_validator
from api.users.dependencies import get_password_validator

from api import create_app


app = create_app()
client = TestClient(app)

class MockCreateUserUseCase:
    def __init__(self):
        pass

    def execute(self, _):
        return {
            "id": 1,
            "email_address": "sample@sample.com",
            "first_name": "Joe",
            "last_name": "Doe",
            "roles": [],
            "classes": [],
        }

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
        pass

    def get_users(self, skip: int, limit: int):
        pass

    def get_user(self, user_id: int):
        pass

def override_database_dependency():
    return MockDatabase()

def override_user_repository_dependency(db = Depends(override_database_dependency)):
    return MockUserRepository(db)

def override_bcrypt_hasher_dependency():
    return MockCreateUserUseCase()

def override_create_user_use_case_dependency():
    return MockCreateUserUseCase()

def override_email_adress_validator_dependency():
    return MockEmailAddressValidator()

def override_password_validator_dependency():
    return MockPasswordValidator()

app.dependency_overrides[get_user_repository] = override_user_repository_dependency
app.dependency_overrides[get_bcrypt_hasher] = override_bcrypt_hasher_dependency
app.dependency_overrides[get_create_user_use_case] = override_create_user_use_case_dependency
app.dependency_overrides[get_email_address_validator] = override_email_adress_validator_dependency
app.dependency_overrides[get_password_validator] = override_password_validator_dependency


def test_given_valid_user_request_when_create_user_is_called_then_status_code_is_200():
    SAMPLE_USER_DATA = {
        "email_address": "sample@sample.com",
        "first_name": "Joe",
        "last_name": "Doe",
        "password": "strathclyde123",
    }

    SAMPLE_RESPONSE_OBJECT = {
        "id": 1,
        "email_address": "sample@sample.com",
        "first_name": "Joe",
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
