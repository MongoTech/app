from app.core.celery_app import celery
from app.core.config import settings
from raven import Client  # type: ignore

client_sentry = Client(settings.SENTRY_DSN)


@celery.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"
