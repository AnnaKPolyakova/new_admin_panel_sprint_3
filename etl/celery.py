import os

from celery import Celery
from celery.schedules import crontab

from config.components.base.base import SETTINGS_FOR_CELERY

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FOR_CELERY)

app = Celery("etl")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "etl.tasks.loader",
        "schedule": crontab(minute=1),
    }
}
