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

def test_when_creating_a_student_with_correct_details_then_student_is_created(
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

    SAMPLE_CLASS_BODY = {
        "reg_no": "myb21881",
        "student_name": "John Doe",
        "year": 1,
        "degree_id": 1
    }

    response = client.post(
        f"/api/v1/students",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 200

def test_given_an_existing_student_when_creating_a_student_with_same_details_then_error_is_thrown(
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

    SAMPLE_CLASS_BODY = {
        "reg_no": "myb21881",
        "student_name": "John Doe",
        "year": 1,
        "degree_id": 1
    }

    response = client.post(
        f"/api/v1/students",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )

    response = client.post(
        f"/api/v1/students",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 409

def test_given_a_user_with_insufficient_permissions_when_creating_a_student_then_error_is_thrown(
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

    SAMPLE_CLASS_BODY = {
        "reg_no": "myb21881",
        "student_name": "John Doe",
        "year": 1,
        "degree_id": 1
    }

    response = client.post(
        f"/api/v1/students",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 403

def test_given_students_when_retrieving_students_then_students_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/students",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_students_in_the_system_when_retrieving_students_then_error_is_thrown(
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

    response = client.get(
        f"/api/v1/students",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_retrieving_students_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/students",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

def test_given_students_when_retrieving_a_student_then_student_is_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_classes(db)
        create_students(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/students/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_non_existing_student_when_retrieving_a_student_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_classes(db)
        create_students(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc91919"

    response = client.get(
        f"/api/v1/students/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_retrieving_a_student_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_classes(db)
        create_students(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/students/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

def test_given_students_when_retrieving_a_students_statistics_then_student_statistics_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_classes(db)
        create_students(db)
        create_marks(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/students/{SAMPLE_STUDENT_REG_NO}/statistics",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_marks_for_student_when_retrieving_a_students_statistics_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_classes(db)
        create_students(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/students/{SAMPLE_STUDENT_REG_NO}/statistics",
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
