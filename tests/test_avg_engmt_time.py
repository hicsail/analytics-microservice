from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_average_engagement_time():
    user_id = "U8765433"
    time_period = 7
    response = client.get(f"/avg_engagement_time/{user_id}/{time_period}")
    assert response.status_code == 200
    assert response.json() == {"user_id": "U8765433", "time_period": 7, "average_engagement_time(sec)": 34}