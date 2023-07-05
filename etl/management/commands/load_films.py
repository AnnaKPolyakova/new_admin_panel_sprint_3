from celery.utils.log import get_task_logger
from django.core.management.base import BaseCommand

from etl.servises.db_updater import DBUpdater


logger = get_task_logger(__name__)


class Command(BaseCommand):
    help = 'Loader'

    def handle(self, *args, **options):
        logger.info("Loader tasks is on")
        updater = DBUpdater()
        updater.update_data_in_elasticsearch()
        logger.info("Loader tasks is finished")
