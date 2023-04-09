import sentry_sdk
from app.core.config import settings
from sentry_sdk.integrations.fastapi import FastApiIntegration


def log_errors(message):  # type: ignore
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENV,
        integrations=[FastApiIntegration()],
    )
    with sentry_sdk.push_scope() as scope:
        sentry_sdk.capture_exception(Exception(message))
        scope.clear()
