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

from scripts.db_base_values import initialise_roles, create_users

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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

def test_given_correct_sample_body_when_creating_a_user_then_user_is_created_succesfully(
        test_db: Generator[None, Any, None]
    ):
    SAMPLE_BODY = {
        "email_address": "test@test.com",
        "first_name": "Kamil",
        "last_name": "Zak",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users",
        json=SAMPLE_BODY
    )
    
    assert response.status_code == 200

def test_given_correct_body_when_logging_in_as_a_user_then_user_is_returned(
        test_db: Generator[None, Any, None]
    ):
    SAMPLE_BODY = {
        "email_address": "test@test.com",
        "first_name": "Kamil",
        "last_name": "Zak",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users",
        json=SAMPLE_BODY
    )
    
    assert response.status_code == 200

    SAMPLE_LOGIN_BODY = {
        "username": "test@test.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200

def test_given_users_in_the_database_when_calling_get_users_then_users_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "admin@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"}
    )
    
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_given_users_in_the_database_when_calling_get_user_with_an_existing_user_then_user_is_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "admin@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    response = client.get(
        f"/api/v1/users/{1}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"}
    )
    
    assert response.status_code == 200

def test_given_a_user_when_editing_the_users_details_then_the_users_details_are_edited(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "admin@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    SAMPLE_EDIT_BODY = {
        "id":"1",
        "first_name": "John",
    }

    response = client.put(
        f"/api/v1/users/{1}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_EDIT_BODY
    )
    
    assert response.status_code == 200
    
def test_given_a_lecturer_when_getting_all_lecturers_then_lecturer_is_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "admin@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    response = client.get(
        f"/api/v1/lecturers",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_given_lecturers_in_the_database_when_calling_get_lecturer_with_an_existing_lecturer_then_lecturer_is_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "admin@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    response = client.get(
        f"/api/v1/lecturers/{1}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"}
    )
    
    assert response.status_code == 200
