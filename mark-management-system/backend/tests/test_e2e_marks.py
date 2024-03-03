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
    create_classes,
    create_degree,
    create_students,
    create_marks
)

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

def test_when_creating_a_mark_with_correct_details_then_mark_is_created(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
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

    SAMPLE_MARK_BODY = {
        "mark": 72,
        "class_id": 1,
        "student_id": 1
    }

    response = client.post(
        f"/api/v1/marks",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_MARK_BODY
    )
    
    assert response.status_code == 200

def test_given_marks_in_the_system_when_retrieving_marks_then_marks_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
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
        f"/api/v1/marks",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_existing_mark_in_the_system_when_retrieving_mark_for_a_student_and_class_then_mark_is_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
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

    SAMPLE_STUDENT_ID = 1
    SAMPLE_CLASS_ID = 1

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_ID}/{SAMPLE_CLASS_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_an_existing_mark_when_editing_the_mark_then_mark_is_edited(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "lecturer@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    SAMPLE_MARK_ID = 1

    SAMPLE_MARK_BODY = {
        "id": 1,
        "mark": 73,
    }

    response = client.put(
        f"/api/v1/marks/{SAMPLE_MARK_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_MARK_BODY
    )
    
    assert response.status_code == 200

def test_given_existing_mark_in_the_system_when_deleting_mark_then_mark_is_deleted(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "lecturer@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    SAMPLE_MARK_ID = 1

    response = client.delete(
        f"/api/v1/marks/{SAMPLE_MARK_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_valid_system_details_when_retrieving_student_statistics_then_statistics_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "lecturer@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    response = client.get(
        f"/api/v1/marks/statistics",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_valid_system_details_when_retrieving_student_statistics_globally_then_statistics_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "lecturer@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    response = client.get(
        f"/api/v1/marks/global/statistics/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_a_valid_student_reg_no_when_retrieving_student_marks_then_marks_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
        db.commit()

    SAMPLE_LOGIN_BODY = {
        "username": "lecturer@mms.com",
        "password": "12345678"
    }

    response = client.post(
        "/api/v1/users/login",
        data=SAMPLE_LOGIN_BODY
    )
    
    assert response.status_code == 200
    JSON_TOKEN = response.json()["access_token"]

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_a_class_code_when_retrieving_student_marks_for_the_class_then_the_marks_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        create_marks(db)
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

    SAMPLE_CLASS_CODE = "CS412"

    response = client.get(
        f"/api/v1/marks/class/{SAMPLE_CLASS_CODE}/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200
