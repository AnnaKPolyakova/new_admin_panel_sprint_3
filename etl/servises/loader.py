import logging

from elasticsearch import Elasticsearch, helpers
from django.conf import settings

from etl.servises.defines import (
    MOVIES_INDEX, MOVIES,
)

logger = logging.getLogger("logger")

LOADER_ERROR = "Loading invalid, error: {error}"


class Loader:

    def __init__(self):
        self.elastic = self._get_elastic()

    @staticmethod
    def _get_elastic():
        url = (
                settings.PROTOCOL + '://' +
                settings.HOSTNAME + ":" +
                str(settings.ELASTICSEARCH_PORT)
        )
        return Elasticsearch(url)

    def index_create(self):
        self.elastic.indices.create(
            index=MOVIES, ignore=400, body=MOVIES_INDEX
        )

    def _load_data(self, data):
        helpers.bulk(self.elastic, data)

    def load_data(self, data):
        self.index_create()
        if len(data) == 0:
            return
        try:
            self._load_data(data)
        except Exception as exeption:
            logger.debug(LOADER_ERROR.format(error=exeption))
            return False
        else:
            logger.debug("Start getting objects for updating")
        return True
