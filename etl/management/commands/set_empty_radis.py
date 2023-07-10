import logging
import os

import redis
from django.core.management.base import BaseCommand

from etl.servises.db_updater import DBUpdater
from etl.servises.defines import MOVIES

logger = logging.getLogger("logger")


class Command(BaseCommand):
    help = 'Loader'

    def handle(self, *args, **options):
        logger.info("Removing on")
        redis_db = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'movies-redis'),
            port=os.environ.get('REDIS_PORT', '6376'),
            db=0
        )
        redis_db.delete(MOVIES)
        logger.info("Removing is finished")
