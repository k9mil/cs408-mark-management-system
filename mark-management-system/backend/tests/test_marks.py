import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from api.marks.controllers.mark_controller import marks

client = TestClient(marks)


def test_index():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}