import logging
import uuid

from django.conf import settings
from psycopg2 import OperationalError
from typing import List, Dict

from etl.servises.backoff import backoff
from etl.servises.extractor import Extractor
from etl.servises.loader import Loader
from etl.servises.transformer import Transformer

logger = logging.getLogger("logger")

LOADED_DATA = "Loaded data for {number} part"
DATA_LOADING_WAS_COMPLETED = "Data loading " \
                             "was completed for all (number) parts"


class DBUpdater:
    def __init__(self):
        self.loader = Loader()
        self.extractor = Extractor()
        self.film_works_ids: List[uuid.UUID] = list()
        self.data_list: List[Dict] = list()

    def _load_data(self, data: List[Dict]):
        self.loader.load_data(data)

    @backoff((OperationalError,))
    @backoff((ConnectionError,))
    def update_data_in_elasticsearch(self):
        logger.debug("Start update data in elasticsearch")
        self.film_works_ids = self.extractor.get_updated_film_works_ids()
        len_data = len(self.film_works_ids)
        if len_data == 0:
            logger.debug("Nothing to update")
            return
        self.data_list = \
            Transformer(self.film_works_ids).film_work_to_list_of_dict()
        count = len_data // settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH
        if count > 0 and len_data % settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH:
            count += 1
        self.loader.index_create()
        for i in range(count):
            data_to_load = self.data_list[
                settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH
                * i: settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH
                * (i + 1)
            ]
            self._load_data(data_to_load)
            logger.debug(LOADED_DATA.format(number=i + 1))
        logger.debug(DATA_LOADING_WAS_COMPLETED.format(numbers=count))
        self.extractor.set_last_data()
