from fastapi.testclient import TestClient
from src.screen_time_stats import app

client = TestClient(app)

def test_screen_time_stats():
    screen_id = 18
    response = client.get(f"/screenTimeStatistics/{screen_id}")
    assert response.status_code == 200
    assert response.json() == {"screen_id": 18, "screen_name": "SCR00221", "total_screen_time(sec)": 60.0,
                                "average_screen_time_per_session(sec)": 60.0}