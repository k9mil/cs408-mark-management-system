import sys
import os
import pytest

from typing import Generator, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from api import create_app

from api.system.models.models import Base
from api.database import engine
from api.config import TestingConfig
from api.database import get_db

from scripts.db_base_values import (
    initialise_roles,
    create_users,
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Some of the code below has been taken in parts from the official FastAPI documentation:

# https://fastapi.tiangolo.com/tutorial/testing/
# https://fastapi.tiangolo.com/advanced/testing-database/

app = create_app()

if TestingConfig.DATABASE_URL:
    engine = create_engine(
        TestingConfig.DATABASE_URL,
    )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

app.dependency_overrides[get_db] = override_get_db

def test_given_a_user_and_a_role_when_adding_a_role_to_a_user_then_user_has_role(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_USER_ROLE_BODY = {
        "user_id": 2,
        "role_id": 1,
    }

    response = client.post(
        f"/api/v1/roles/1/user/2",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_USER_ROLE_BODY
    )
    
    assert response.status_code == 200

def test_given_non_admin_request_when_adding_a_role_to_a_user_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_USER_ROLE_BODY = {
        "user_id": 2,
        "role_id": 1,
    }

    response = client.post(
        f"/api/v1/roles/1/user/2",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_USER_ROLE_BODY
    )
    
    assert response.status_code == 403

def test_given_non_existing_role_when_adding_a_role_to_a_user_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_USER_ROLE_BODY = {
        "user_id": 2,
        "role_id": 10,
    }

    response = client.post(
        f"/api/v1/roles/10/user/2",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_USER_ROLE_BODY
    )
    
    assert response.status_code == 404

def test_given_user_has_role_when_adding_same_role_to_a_user_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_USER_ROLE_BODY = {
        "user_id": 2,
        "role_id": 2,
    }

    response = client.post(
        f"/api/v1/roles/1/user/2",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_USER_ROLE_BODY
    )
    
    response = client.post(
        f"/api/v1/roles/1/user/2",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_USER_ROLE_BODY
    )
    
    assert response.status_code == 409

def test_given_a_user_with_a_role_when_removing_a_role_from_a_user_then_users_role_has_been_removed(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.delete(
        f"/api/v1/roles/1/user/1",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_a_user_with_insufficient_permissions_when_removing_a_role_from_a_user_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.delete(
        f"/api/v1/roles/1/user/2",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

def test_given_a_non_existing_role_when_removing_a_role_from_a_user_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.delete(
        f"/api/v1/roles/100/user/2",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_user_does_not_have_role_when_removing_a_role_from_a_user_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.delete(
        f"/api/v1/roles/1/user/3",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def _prepare_login_and_retrieve_token(
    username: str,
    password: str
) -> str:
    SAMPLE_LOGIN_BODY = {"username": username, "password": password}
    response = client.post("/api/v1/users/login", data=SAMPLE_LOGIN_BODY)

    assert response.status_code == 200
    return response.json()["access_token"]
