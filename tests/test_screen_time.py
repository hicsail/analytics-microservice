from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_user_screen_time():
    user_id = "U8765433"
    screen_id = 18
    response = client.get(f"/screen_time/{user_id}/{screen_id}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "screen_id": screen_id, "screen_time(sec)": 120.0}

def test_get_user_screen_time_no_user():
    user_id = "U876543"
    screen_id = 18
    response = client.get(f"/screen_time/{user_id}/{screen_id}")
    assert response.status_code == 404
    assert response.json() == {"message": "User not Found."}

def test_screen_time_stats():
    screen_id = 18
    response = client.get(f"/screen_time/{screen_id}")
    assert response.status_code == 200
    assert response.json() == {"screen_id": 18, "screen_name": "SCR00221", "total_screen_time(sec)": 60.0,
                                "average_screen_time_per_session(sec)": 60.0}
