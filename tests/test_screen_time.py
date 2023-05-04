from fastapi.testclient import TestClient
from src.user_screen_time import app

client = TestClient(app)

def test_get_screen_time():
    user_id = "U8765433"
    screen_id = 18
    response = client.get(f"/screenTime/{user_id}/{screen_id}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "screen_id": screen_id, "screen_time(sec)": 120.0}