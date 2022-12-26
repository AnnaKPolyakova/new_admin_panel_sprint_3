import datetime

from django.conf import settings
import redis

from etl.servises.defines import LAST_EXTRACT_DATA
from movies.models import (
    Genre,
    Person,
    FilmWork,
    GenreFilmWork,
    PersonFilmWork,
)

MODELS = [
    Genre,
    Person,
    FilmWork,
    GenreFilmWork,
    PersonFilmWork,
]


class PostgresExtractor:
    def __init__(self):
        self.redis_db = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )
        self.last_extract_data = self._get_last_data()

    def _get_last_data(self):
        data = self.redis_db.get(LAST_EXTRACT_DATA)
        if not data:
            return
        data = data.decode("utf-8")
        return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f")

    def _set_last_data(self, data):
        self.redis_db.set(LAST_EXTRACT_DATA, data)

    def extract_data(self):
        for model in MODELS:
            pass
