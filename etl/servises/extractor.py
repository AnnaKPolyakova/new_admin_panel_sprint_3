import datetime
import logging

from django.conf import settings
import redis

from etl.servises.defines import (
    LAST_EXTRACT_DATA_FOR_FILM_WORK,
    LAST_EXTRACT_DATA_FOR_PERSON,
    LAST_EXTRACT_DATA_FOR_GENRE,
)

from movies.models import (
    Genre,
    Person,
    FilmWork,
)

MODELS_AND_FILTERS_FIELDS = {
    LAST_EXTRACT_DATA_FOR_FILM_WORK: "modified__gt",
    LAST_EXTRACT_DATA_FOR_PERSON:
        "person_film_work__person__modified__gt",
    LAST_EXTRACT_DATA_FOR_GENRE:
        "genre_film_work__genre__modified__gt",
}

MODELS_AND_DATA_FIELDS ={
    FilmWork: LAST_EXTRACT_DATA_FOR_FILM_WORK,
    Genre: LAST_EXTRACT_DATA_FOR_GENRE,
    Person: LAST_EXTRACT_DATA_FOR_PERSON,
}

logger = logging.getLogger("logger")

FINISHED_GETTING_OBJECTS = (
    "Finished getting objects for updating. Total count: {count}"
)
NEW_DATES_SET = "New date {date} for updating was set for {obj_name}"


class Extractor:
    def __init__(self):
        self.redis_db = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )
        self.film_new_date = None
        self.genre_new_date = None
        self.person_new_date = None
        self._new_objects_set = set()

    def _get_last_data(self, key_name):
        data = self.redis_db.get(key_name)
        if not data:
            return
        data = data.decode("utf-8")
        return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f%z")

    def set_last_data(self):
        if self.film_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_FILM_WORK, str(self.film_new_date)
            )
            logger.debug(NEW_DATES_SET.format(
                date=self.film_new_date,
                obj_name=LAST_EXTRACT_DATA_FOR_FILM_WORK)
            )
        if self.genre_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_GENRE, str(self.genre_new_date)
            )
            logger.debug(NEW_DATES_SET.format(
                date=self.genre_new_date, obj_name=LAST_EXTRACT_DATA_FOR_GENRE)
            )
        if self.person_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_PERSON, str(self.person_new_date)
            )
            logger.debug(NEW_DATES_SET.format(
                date=self.person_new_date,
                obj_name=LAST_EXTRACT_DATA_FOR_PERSON)
            )

    def _get_filters(self, key_name):
        data = self._get_last_data(key_name)
        if data is not None:
            return {MODELS_AND_FILTERS_FIELDS[key_name]: data}
        return dict()

    def _get_new_film_work(self):
        filters = self._get_filters(LAST_EXTRACT_DATA_FOR_FILM_WORK)
        queryset = FilmWork.objects.prefetch_related(
            "genres",
            "persons"
        ).filter(**filters).order_by("modified")
        if queryset.count() == 0:
            return queryset
        self.film_new_date = queryset.filter(
                modified__isnull=False
            ).last().modified
        return queryset

    def _get_film_work_with_updated_person(self):
        filters = self._get_filters(LAST_EXTRACT_DATA_FOR_PERSON)
        queryset = FilmWork.objects.prefetch_related(
            "genres",
            "persons"
        ).filter(**filters).order_by("person_film_work__person__modified")
        if queryset.count() == 0:
            return queryset
        self.person_new_date = max(
            queryset.filter(
                persons__modified__isnull=False
            ).values_list("persons__modified", flat=True)
        )
        return queryset

    def _get_film_work_with_updated_genres(self):
        filters = self._get_filters(LAST_EXTRACT_DATA_FOR_GENRE)
        queryset = FilmWork.objects.prefetch_related(
            "genres",
            "persons"
        ).filter(**filters).order_by("genre_film_work__genre__modified")
        if queryset.count() == 0:
            return queryset
        self.genre_new_date = max(
            queryset.filter(
                genres__modified__isnull=False
            ).values_list("genres__modified", flat=True)
        )
        return queryset

    def get_updated_film_work_queryset(self):
        logger.debug("Start getting objects for updating")
        film_work_queryset = self._get_new_film_work()
        queryset_with_updated_person = self._get_film_work_with_updated_person()
        queryset_with_updated_genres = self._get_film_work_with_updated_genres()
        film_work_queryset.union(
            queryset_with_updated_person, queryset_with_updated_genres
        )
        count = film_work_queryset.count()
        logger.debug(FINISHED_GETTING_OBJECTS.format(count=count))
        return film_work_queryset
