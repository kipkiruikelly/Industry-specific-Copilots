import os
from src.config import settings

# Celery app stub for background processing queues
try:
    from celery import Celery

    celery_app = Celery(
        "medicopilot_tasks",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )

    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
except ImportError:
    celery_app = None
