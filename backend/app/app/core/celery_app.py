from celery import Celery  # type: ignore

from app.core.config import Settings

MONGO_URL = f"{Settings.MONGO_USER}:{Settings.MONGO_PASS}@{Settings.MONGO_HOST}:27017"
from app.core.config import settings

MONGO_URL = f"{settings.MONGO_USER}:{settings.MONGO_PASS}@{settings.MONGO_HOST}:27017"
OPTIONS = "authSource=admin&retryWrites=true&w=majority"

celery = Celery(
    "EOD_TASKS",
    broker=f"mongodb://{MONGO_URL}/{Settings.MONGO_DB}?{OPTIONS}",
    broker=f"mongodb://{MONGO_URL}/{settings.MONGO_DB}?{OPTIONS}",
)
