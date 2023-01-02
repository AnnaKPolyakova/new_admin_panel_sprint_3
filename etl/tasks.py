import logging

from celery.result import AsyncResult
from django.conf import settings
import redis

from etl.celery import app
from etl.servises.db_updater import DBUpdater
from etl.servises.defines import TASK_ID

logger = logging.getLogger("logger")


@app.task()
def loader():
    logger.info("Loader tasks is on")
    redis_db = redis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
    )
    task_id = redis_db.get(TASK_ID)
    if task_id:
        task_result = AsyncResult("task_id")
        logger.info(f"Task status: {task_result.result}")
        if task_result.result is not True:
            return
    updater = DBUpdater()
    updater.update_data_in_elasticsearch()
