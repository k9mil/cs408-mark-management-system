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
    create_marks,
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

def test_when_creating_academic_misconducts_with_correct_details_then_academic_misconducts_are_created(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_degree(db)
        create_students(db)
        create_users(db)
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

    SAMPLE_ACADEMIC_MISCONDUCT_BODY = {
        "date": "2024-03-03",
        "outcome": "UPHELD",
        "reg_no": "abc12345",
        "class_code": "CS412"
    }

    response = client.post(
        f"/api/v1/academic-misconducts",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_ACADEMIC_MISCONDUCT_BODY
    )
    
    assert response.status_code == 200

def test_when_creating_academic_misconducts_with_wrong_student_reg_no_then_student_not_found_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_degree(db)
        create_students(db)
        create_users(db)
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

    SAMPLE_ACADEMIC_MISCONDUCT_BODY = {
        "date": "2024-03-03",
        "outcome": "UPHELD",
        "reg_no": "jah98765",
        "class_code": "CS412"
    }

    response = client.post(
        f"/api/v1/academic-misconducts",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_ACADEMIC_MISCONDUCT_BODY
    )
    
    assert response.status_code == 404

def test_when_creating_academic_misconducts_with_wrong_student_class_code_then_class_not_found_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_degree(db)
        create_students(db)
        create_users(db)
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

    SAMPLE_ACADEMIC_MISCONDUCT_BODY = {
        "date": "2024-03-03",
        "outcome": "UPHELD",
        "reg_no": "abc12345",
        "class_code": "CS919"
    }

    response = client.post(
        f"/api/v1/academic-misconducts",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_ACADEMIC_MISCONDUCT_BODY
    )
    

    assert response.status_code == 404

def test_when_creating_academic_misconducts_with_same_misconduct_existing_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_degree(db)
        create_students(db)
        create_users(db)
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

    SAMPLE_ACADEMIC_MISCONDUCT_BODY = {
        "date": "2024-03-03",
        "outcome": "UPHELD",
        "reg_no": "abc12345",
        "class_code": "CS412"
    }

    response = client.post(
        f"/api/v1/academic-misconducts",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_ACADEMIC_MISCONDUCT_BODY
    )

    response = client.post(
        f"/api/v1/academic-misconducts",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_ACADEMIC_MISCONDUCT_BODY
    )
    
    assert response.status_code == 409

def test_when_creating_academic_misconducts_when_student_not_belong_to_class_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_degree(db)
        create_students(db)
        create_users(db)
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

    SAMPLE_ACADEMIC_MISCONDUCT_BODY = {
        "date": "2024-03-03",
        "outcome": "UPHELD",
        "reg_no": "abc12345",
        "class_code": "CS408"
    }

    response = client.post(
        f"/api/v1/academic-misconducts",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_ACADEMIC_MISCONDUCT_BODY
    )
    
    assert response.status_code == 404
