from fastapi.testclient import TestClient
from app.core.config import settings
from app.tests.utils.db import fake_db
from app.main import app
from app.api.deps import get_db
app.dependency_overrides[get_db] = fake_db


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
