import json
from src.main import *
from fastapi.testclient import TestClient
import uuid
from src.user import *
from src.user import app


client = TestClient(app)


def test_add_user_successfully():
    id = uuid.uuid4()
    payload = {"userID":str(id)}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 200
    json_response = json.loads(response.content.decode('utf-8'))
    assert json_response['status code'] == 200
    assert json_response['message'] == "Added user successfully"
    delete_user_from_database(str(id))


def test_add_duplicate_user():
    try:
        id = uuid.uuid4()
        payload = {"userID":str(id)}
        response = client.post("/api/analysis/add-user/",json=payload)
        assert response.status_code == 200
        response = client.post("/api/analysis/add-user/",json=payload)
        assert response.status_code == 413
        delete_user_from_database(str(id))
    except HTTPException as e:
        print(e)
        assert False


def test_missing_user_id_field():
    payload = {"userID": ""}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 411


def test_add_user_userid_not_uuid():
    not_user_id = "not_uuid"
    payload = {"userID": not_user_id}
    response = client.post("/api/analysis/add-user/",json=payload)
    assert response.status_code == 412
