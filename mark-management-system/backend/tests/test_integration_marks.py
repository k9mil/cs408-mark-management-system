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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

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

def test_given_an_existing_mark_when_creating_a_mark_with_same_details_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

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

    response = client.post(
        f"/api/v1/marks",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_MARK_BODY
    )
    
    assert response.status_code == 409

def test_given_a_user_with_insufficient_permissions_when_creating_a_mark_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

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
    
    assert response.status_code == 403

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_marks_in_the_system_when_retrieving_marks_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_retrieving_marks_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_STUDENT_ID = 1
    SAMPLE_CLASS_ID = 1

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_ID}/{SAMPLE_CLASS_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_non_existing_data_when_retrieving_mark_for_a_student_and_class_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_STUDENT_ID = 101
    SAMPLE_CLASS_ID = 202

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_ID}/{SAMPLE_CLASS_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_retrieving_mark_for_a_student_and_class_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    SAMPLE_STUDENT_ID = 1
    SAMPLE_CLASS_ID = 1

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_ID}/{SAMPLE_CLASS_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

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

def test_given_a_non_existing_mark_when_editing_the_mark_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_MARK_ID = 1

    SAMPLE_MARK_BODY = {
        "id": 919,
        "mark": 73,
    }

    response = client.put(
        f"/api/v1/marks/{SAMPLE_MARK_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
        json=SAMPLE_MARK_BODY
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_editing_the_mark_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

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
    
    assert response.status_code == 403

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_MARK_ID = 1

    response = client.delete(
        f"/api/v1/marks/{SAMPLE_MARK_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_a_nonexisting_mark_in_the_system_when_deleting_mark_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_MARK_ID = 7191

    response = client.delete(
        f"/api/v1/marks/{SAMPLE_MARK_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_deleting_mark_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    SAMPLE_MARK_ID = 1

    response = client.delete(
        f"/api/v1/marks/{SAMPLE_MARK_ID}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks/statistics",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_marks_in_the_system_when_retrieving_student_statistics_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks/statistics",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks/global/statistics/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_no_marks_in_the_system_details_when_retrieving_student_statistics_globally_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks/global/statistics/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_a_user_with_insufficient_permissions_when_retrieving_student_statistics_globally_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "base@mms.com", "12345678"
    )

    response = client.get(
        f"/api/v1/marks/global/statistics/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_an_invalid_student_reg_no_when_retrieving_student_marks_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc91919"

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

def test_given_no_marks_in_the_system_when_retrieving_student_marks_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_STUDENT_REG_NO = "abc12345"

    response = client.get(
        f"/api/v1/marks/{SAMPLE_STUDENT_REG_NO}",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 404

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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_CODE = "CS412"

    response = client.get(
        f"/api/v1/marks/class/{SAMPLE_CLASS_CODE}/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 200

def test_given_a_user_with_insufficient_permissions_when_retrieving_student_marks_for_the_class_then_error_is_thrown(
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

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "lecturer@mms.com", "12345678"
    )

    SAMPLE_CLASS_CODE = "CS412"

    response = client.get(
        f"/api/v1/marks/class/{SAMPLE_CLASS_CODE}/all",
        headers={"Authorization": f"Bearer {JSON_TOKEN}"},
    )
    
    assert response.status_code == 403

def test_given_no_marks_in_the_system_when_retrieving_student_marks_for_the_class_then_error_is_thrown(
        test_db: Generator[None, Any, None]
    ):
    with TestingSessionLocal() as db:
        initialise_roles(db)
        create_users(db)
        create_degree(db)
        create_students(db)
        create_classes(db)
        db.commit()

    JSON_TOKEN = _prepare_login_and_retrieve_token(
        "admin@mms.com", "12345678"
    )

    SAMPLE_CLASS_CODE = "CS412"

    response = client.get(
        f"/api/v1/marks/class/{SAMPLE_CLASS_CODE}/all",
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
