from etl.celery import app
from etl.servises.db_updater import DBUpdater
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@app.task()
def loader():
    logger.info("Loader tasks is on")
    updater = DBUpdater()
    updater.update_data_in_elasticsearch()
    logger.info("Loader tasks is finished")
