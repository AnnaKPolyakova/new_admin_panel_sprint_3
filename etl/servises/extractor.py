import datetime

from django.conf import settings
import redis

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

from etl.servises.defines import (
    LAST_EXTRACT_DATA_FOR_FILM_WORK,
    LAST_EXTRACT_DATA_FOR_PERSON,
    LAST_EXTRACT_DATA_FOR_GENRE,
)
#
# MODELS_AND_DATA_FIELDS = {
#     FilmWork: LAST_EXTRACT_DATA_FOR_FILM_WORK,
#     Person: LAST_EXTRACT_DATA_FOR_PERSON,
#     Genre: LAST_EXTRACT_DATA_FOR_GENRE,
# }


class PostgresExtractor:
    def __init__(self):
        self.redis_db = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )
        self.last_extract_data = self._get_last_data()
        self.new_date = None

    def _get_last_data(self, key_name):
        data = self.redis_db.get(key_name)
        if not data:
            return
        data = data.decode("utf-8")
        return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f")

    def _set_last_data(self, model, data):
        self.redis_db.set(model, data)

    def _get_filters(self, key_name):
        data = self._get_last_data(key_name)
        if data is not None:
            return {"modified__gte": data}
        return dict()

    def _get_film_work(self):
        filters = self._get_filters(LAST_EXTRACT_DATA_FOR_FILM_WORK)
        queryset = FilmWork.objects.prefetch_related(
            "genres",
            "people"
        ).filter(**filters).order_by("modified")[
            settings.SIZE_FOR_LOAD_TO_ELASTICSEARCH
        ]
        self.new_date = queryset.lasr.modified
        return queryset

    def extract_data(self):
        queryset = self._get_film_work()
        if queryset.count() > 0:
            pass



