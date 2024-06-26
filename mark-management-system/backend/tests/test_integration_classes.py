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

def test_when_creating_a_class_with_correct_details_then_class_is_created(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_BODY = {
        "lecturer_id": 1,
        "name": "Sample Class",
        "code": "CS101",
        "credit": 10,
        "credit_level": 1,
    }

    response = client.post(
        f"/api/v1/classes",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 200

def test_given_an_existing_class_when_creating_same_class_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_BODY = {
        "lecturer_id": 1,
        "name": "Sample Class",
        "code": "CS101",
        "credit": 10,
        "credit_level": 1,
    }

    response = client.post(
        f"/api/v1/classes",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )

    response = client.post(
        f"/api/v1/classes",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 409

def test_given_requestor_is_lecturer_when_creating_class_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_CLASS_BODY = {
        "lecturer_id": 1,
        "name": "Sample Class",
        "code": "CS101",
        "credit": 10,
        "credit_level": 1,
    }

    response = client.post(
        f"/api/v1/classes",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 403

def test_given_classes_in_the_system_when_retrieving_classes_then_classes_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/classes",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_classes_in_the_system_when_retrieving_classes_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/classes",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_requestor_is_lecturer_when_retrieving_classes_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/classes",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

def test_given_classes_in_the_system_when_retrieving_classes_for_lecturer_then_classes_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/classes/lecturer",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_classes_in_the_system_when_retrieving_classes_for_lecturer_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/classes/lecturer",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_an_existing_class_when_editing_the_class_then_class_is_edited(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_BODY = {
        "id": 1,
        "original_code": "CS412",
        "lecturer_id": 1,
        "name": "New Name",
        "code": "New Code",
        "credit": 10,
        "credit_level": 2,
    }

    response = client.put(
        f"/api/v1/classes/1",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 200

def test_given_an_existing_class_when_editor_is_not_admin_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_CLASS_BODY = {
        "id": 1,
        "original_code": "CS412",
        "lecturer_id": 1,
        "name": "New Name",
        "code": "New Code",
        "credit": 10,
        "credit_level": 2,
    }

    response = client.put(
        f"/api/v1/classes/1",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 403

def test_given_an_existing_class_when_editing_the_class_with_a_code_which_exists_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_BODY = {
        "id": 1,
        "original_code": "CS412",
        "lecturer_id": 1,
        "name": "New Name",
        "code": "CS408",
        "credit": 10,
        "credit_level": 2,
    }

    response = client.put(
        f"/api/v1/classes/1",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 409

def test_given_a_class_code_when_editing_when_class_code_doesnt_exist_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_BODY = {
        "id": 1237312656,
        "original_code": "CS491",
        "lecturer_id": 1,
        "name": "New Name",
        "code": "CS101",
        "credit": 10,
        "credit_level": 2,
    }

    response = client.put(
        f"/api/v1/classes/1237312656",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_CLASS_BODY
    )
    
    assert response.status_code == 404

def test_given_an_existing_class_when_deleting_the_class_then_class_is_deleted(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
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

        response = client.delete(
            f"/api/v1/classes/1",
            headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        )
        
        assert response.status_code == 200

def test_given_an_existing_class_when_deleting_the_class_with_no_admin_role_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.delete(
        f"/api/v1/classes/1",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

def test_given_a_class_code_which_doesnt_exist_when_deleting_the_class_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.delete(
        f"/api/v1/classes/9986123",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403
    
def test_given_an_existing_class_when_class_is_retrieved_then_details_of_the_class_are_returned(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_CODE = "CS412"

    response = client.get(
        f"/api/v1/classes/{SAMPLE_CLASS_CODE}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_a_non_existing_class_code_when_class_is_retrieved_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_CODE = "CS919"

    response = client.get(
        f"/api/v1/classes/{SAMPLE_CLASS_CODE}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_class_when_retrieving_statistics_of_that_class_then_statistics_are_returned(
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

    SAMPLE_CLASS_CODE = "CS412"

    response = client.get(
        f"/api/v1/classes/{SAMPLE_CLASS_CODE}/statistics",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_marks_in_the_system_when_retrieving_statistics_of_that_class_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_CODE = "CS412"

    response = client.get(
        f"/api/v1/classes/{SAMPLE_CLASS_CODE}/statistics",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_classes_in_the_system_when_retrieving_metrics_of_that_class_then_metrics_are_returned(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/classes/metrics/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_marks_in_the_system_when_retrieving_metrics_of_that_class_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/classes/metrics/all",
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
