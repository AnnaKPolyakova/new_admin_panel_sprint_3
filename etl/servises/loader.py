from elasticsearch import Elasticsearch
from django.conf import settings

from etl.servises.defines import (
    MOVIES_INDEX,
)


class Loader:

    def __init__(self):
        self.elastic = self._get_elastic()

    @staticmethod
    def _get_elastic():
        url = (
                settings.PROTOCOL + '://' +
                settings.HOSTNAME + ":" +
                str(settings.PORT)
        )
        return Elasticsearch(url)

    def _index_create(self):
        self.elastic.indices.create(
            index='movies', ignore=400, body=MOVIES_INDEX
        )