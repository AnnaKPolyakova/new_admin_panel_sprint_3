import logging

from django.conf import settings

from etl.servises.extractor import Extractor
from etl.servises.loader import Loader
from etl.servises.transformer import Transformer
from movies.models import FilmWork

logger = logging.getLogger("logger")

LOADED_DATA = "Loaded data for {number} part"
DATA_LOADING_WAS_COMPLETED = "Data loading was completed for all (number) parts"


class DBUpdater:

    def __init__(self):
        self.loader = Loader()
        self.extractor = Extractor()
        self.film_work_qs = FilmWork.objects.none()
        self.data_list = list()

    def _load_data(self, data):
        self.loader.load_data(data)

    def update_data_in_elasticsearch(self):
        logger.debug("Start update data in elasticsearch")
        self.film_work_qs = self.extractor.get_updated_film_work_queryset()
        len_data = len(self.film_work_qs)
        if len_data == 0:
            logger.debug("Nothing to update")
            return
        self.data_list = Transformer(
            self.film_work_qs
        ).film_work_to_list_of_dict()
        count = len_data // settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH
        if count > 0 and len_data % settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH:
            count += 1
        for i in range(count):
            data_to_load = self.data_list[
                settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH * i:
                settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH * (i + 1)
            ]
            self._load_data(data_to_load)
            logger.debug(LOADED_DATA.format(number=i + 1))
        logger.debug(DATA_LOADING_WAS_COMPLETED.format(numbers=count))
        self.extractor.set_last_data()

