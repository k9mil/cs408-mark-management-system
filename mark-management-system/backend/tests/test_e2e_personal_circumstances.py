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
    create_personal_circumstances
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

def test_when_creating_personal_circumstances_with_correct_details_then_personal_circumstances_are_created(
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

    SAMPLE_PERSONAL_CIRCUMSTANCES_BODY = {
        "details": "03/31/2023 to 05/29/2024: Mental Health Issues",
        "semester": "2",
        "cat": "2",
        "comments": "Discount attempt as CS412",
        "reg_no": "abc54321"
    }

    response = client.post(
        f"/api/v1/personal-circumstances",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_PERSONAL_CIRCUMSTANCES_BODY
    )
    
    assert response.status_code == 200

def test_given_student_reg_no_when_retrieving_personal_circumstances_for_student_then_personal_circumstances_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_degree(db)
        create_students(db)
        create_users(db)
        create_classes(db)
        create_marks(db)  
        create_personal_circumstances(db)
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

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/personal-circumstances/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200