import logging

from django.conf import settings
from elasticsearch import Elasticsearch, helpers
from typing import Dict

from etl.servises.defines import MOVIES, MOVIES_INDEX

logger = logging.getLogger("logger")

LOADER_ERROR = "Loading invalid, error: {error}"


class Loader:
    def __init__(self):
        self.elastic: Elasticsearch = self._get_elastic()

    @staticmethod
    def _get_elastic():
        url = (
            settings.ELASTICSEARCH_PROTOCOL
            + "://"
            + settings.ELASTICSEARCH_HOSTNAME
            + ":"
            + str(settings.ELASTICSEARCH_PORT)
        )
        return Elasticsearch(url)

    def index_create(self):
        self.elastic.indices.create(
            index=MOVIES, ignore=400, body=MOVIES_INDEX
        )

    def _load_data(self, data: Dict):
        helpers.bulk(self.elastic, data)

    def load_data(self, data: Dict):
        if len(data) == 0:
            return
        try:
            self._load_data(data)
        except Exception as error:
            msg = "Loading get error {error}"
            logger.debug(msg.format(error=error))
            self._load_data(data)
        logger.debug("loading done")
        return
