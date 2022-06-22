from typing import Dict
from fastapi.testclient import TestClient
from app.core.config import settings
import pytest  # type: ignore
from app.tests.utils.db import fake_db
from app.main import app
from app.api.deps import get_db
app.dependency_overrides[get_db] = fake_db



@pytest.mark.asyncio
async def notest_celery_worker_test(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    data = {"msg": "test"}
    r = client.post(
        f"{settings.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
