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
    create_degree,
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

def test_when_creating_a_degree_with_correct_details_then_degree_is_created(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_DEGREE_BODY = {
        "level": "BSc (Hons)",
        "name": "Computer Science",
        "code": "0403",
    }

    response = client.post(
        f"/api/v1/degrees",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_DEGREE_BODY
    )
    
    assert response.status_code == 200

def test_given_a_degree_in_the_system_when_creating_a_degree_with_same_details_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_DEGREE_BODY = {
        "level": "BSc (Hons)",
        "name": "Computer Science",
        "code": "0403",
    }

    response = client.post(
        f"/api/v1/degrees",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_DEGREE_BODY
    )

    response = client.post(
        f"/api/v1/degrees",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_DEGREE_BODY
    )
    
    assert response.status_code == 409

def test_given_not_an_administrator_when_creating_a_degree_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_DEGREE_BODY = {
        "level": "BSc (Hons)",
        "name": "Computer Science",
        "code": "0403",
    }

    response = client.post(
        f"/api/v1/degrees",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_DEGREE_BODY
    )
    
    assert response.status_code == 403

def test_given_degrees_when_retrieving_a_degree_with_then_degree_is_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_DEGREE_NAME = "Computer Science"

    response = client.get(
        f"/api/v1/degrees/{SAMPLE_DEGREE_NAME}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200
    
def test_given_non_existing_degree_name_when_retrieving_degree_details_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_DEGREE_NAME = "Computer Sciance"

    response = client.get(
        f"/api/v1/degrees/{SAMPLE_DEGREE_NAME}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_retrieving_degree_details_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    SAMPLE_DEGREE_NAME = "Computer Science"

    response = client.get(
        f"/api/v1/degrees/{SAMPLE_DEGREE_NAME}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403
    
def test_given_valid_degrees_when_searching_in_bulk_then_degrees_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_DEGREE_JSON = [
        {
            "level": "BSc (Hons)",
            "name": "Computer Science",
            "code": "0403",
        }
    ]

    response = client.post(
        f"/api/v1/degrees/search",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_DEGREE_JSON
    )
    
    assert response.status_code == 200

def test_given_an_invalid_degree_when_searching_in_bulk_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        db.commit()
    
    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_DEGREE_JSON = [
        {
            "level": "BSc (Hons)",
            "name": "Computer Sciance",
            "code": "0404",
        }
    ]

    response = client.post(
        f"/api/v1/degrees/search",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_DEGREE_JSON
    )
    
    assert response.status_code == 404

def test_given_given_a_user_with_insufficient_permissions_when_searching_in_bulk_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    SAMPLE_DEGREE_JSON = [
        {
            "level": "BSc (Hons)",
            "name": "Computer Science",
            "code": "0403",
        }
    ]

    response = client.post(
        f"/api/v1/degrees/search",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_DEGREE_JSON
    )
    
    assert response.status_code == 403

def _prepare_login_and_retrieve_token(
    username: str,
    password: str
) -> str:
    SAMPLE_LOGIN_BODY = {"username": username, "password": password}
    response = client.post("/api/v1/users/login", data=SAMPLE_LOGIN_BODY)

    assert response.status_code == 200
    return response.json()["access_token"]
