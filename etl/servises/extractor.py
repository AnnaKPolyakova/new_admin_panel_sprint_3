import datetime
import logging
from django.db import connection

import redis
from django.conf import settings
from typing import Set

from etl.servises.defines import (
    LAST_EXTRACT_DATA_FOR_FILM_WORK,
    LAST_EXTRACT_DATA_FOR_GENRE,
    LAST_EXTRACT_DATA_FOR_PERSON,
)
from movies.models import FilmWork, Genre, Person

MODELS_AND_FILTERS_FIELDS = {
    LAST_EXTRACT_DATA_FOR_FILM_WORK: "modified__gt",
    LAST_EXTRACT_DATA_FOR_PERSON: "person_film_work__person__modified__gt",
    LAST_EXTRACT_DATA_FOR_GENRE: "genre_film_work__genre__modified__gt",
}

MODELS_AND_DATA_FIELDS = {
    FilmWork: LAST_EXTRACT_DATA_FOR_FILM_WORK,
    Genre: LAST_EXTRACT_DATA_FOR_GENRE,
    Person: LAST_EXTRACT_DATA_FOR_PERSON,
}

logger = logging.getLogger("logger")

FINISHED_GETTING_OBJECTS = "Finished getting objects for updating. " \
                           "Total count: {count}"
NEW_DATES_SET = "New date {date} for updating was set for {obj_name}"


class Extractor:
    def __init__(self):
        self.redis_db: redis.Redis = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
        )
        self.film_new_date: datetime = None
        self.genre_new_date: datetime = None
        self.person_new_date: datetime = None
        self._new_objects_set: Set[FilmWork] = set()

    def _get_last_data(self, key_name: str):
        data = self.redis_db.get(key_name)
        if not data:
            return
        data = data.decode("utf-8")
        return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f%z")

    def set_last_data(self):
        if self.film_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_FILM_WORK,
                str(self.film_new_date)
            )
            logger.debug(
                NEW_DATES_SET.format(
                    date=self.film_new_date,
                    obj_name=LAST_EXTRACT_DATA_FOR_FILM_WORK
                )
            )
        if self.genre_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_GENRE,
                str(self.genre_new_date)
            )
            logger.debug(
                NEW_DATES_SET.format(
                    date=self.genre_new_date,
                    obj_name=LAST_EXTRACT_DATA_FOR_GENRE
                )
            )
        if self.person_new_date:
            self.redis_db.set(
                LAST_EXTRACT_DATA_FOR_PERSON,
                str(self.person_new_date)
            )
            logger.debug(
                NEW_DATES_SET.format(
                    date=self.person_new_date,
                    obj_name=LAST_EXTRACT_DATA_FOR_PERSON
                )
            )

    @staticmethod
    def _get_sql_request(sql: str, date: str):
        with connection.cursor() as cursor:
            cursor.execute(sql, [date])
            columns = [col[0] for col in cursor.description]
            cursor = cursor.fetchall()
            rows = [dict(zip(columns, row)) for row in cursor]
        return rows

    def _get_new_film_works_ids(self):
        date = self._get_last_data(LAST_EXTRACT_DATA_FOR_FILM_WORK)
        sql = (
            "SELECT id, modified "
            "FROM content.film_work as fw "
            "{filter} "
            "ORDER BY fw.modified ASC "
        )
        if date is None:
            sql = sql.format(filter=" ")
        else:
            sql = sql.format(filter="WHERE fw.modified >  %s ")
        objects = self._get_sql_request(sql, date)
        if len(objects) > 0:
            self.film_new_date = max(obj["modified"] for obj in objects)
        return set(str(obj["id"]) for obj in objects)

    def _get_film_work_with_updated_person(self):
        date = self._get_last_data(LAST_EXTRACT_DATA_FOR_PERSON)
        sql = (
            "SELECT pfw.film_work_id, p.modified "
            "FROM content.person as p "
            "LEFT JOIN content.person_film_work as pfw "
            "ON p.id = pfw.person_id "
            "{filter} "
            "ORDER BY p.modified ASC "
        )
        if date is None:
            sql = sql.format(filter=" ")
        else:
            sql = sql.format(filter="WHERE p.modified >  %s ")
        objects = self._get_sql_request(sql, date)
        if len(objects) > 0:
            self.person_new_date = max(obj["modified"] for obj in objects)
        return set(str(obj["film_work_id"]) for obj in objects)

    def _get_film_work_with_updated_genres(self):
        date = self._get_last_data(LAST_EXTRACT_DATA_FOR_GENRE)
        sql = (
            "SELECT gfw.film_work_id, g.modified "
            "FROM content.genre as g "
            "LEFT JOIN content.genre_film_work as gfw "
            "ON g.id = gfw.genre_id "
            "{filter} "
            "ORDER BY g.modified ASC "
        )
        if date is None:
            sql = sql.format(filter=" ")
        else:
            sql = sql.format(filter="WHERE g.modified >  %s ")
        objects = self._get_sql_request(sql, date)
        if len(objects) > 0:
            self.genre_new_date = max(obj["modified"] for obj in objects)
        return set(str(obj["film_work_id"]) for obj in objects)

    def get_updated_film_works_ids(self):
        logger.debug("Start getting objects for updating")
        film_works_ids = self._get_new_film_works_ids()
        film_works_ids_with_updated_person = \
            self._get_film_work_with_updated_person()
        film_works_ids_with_updated_genres = \
            self._get_film_work_with_updated_genres()
        film_works_ids.union(
            film_works_ids_with_updated_person,
            film_works_ids_with_updated_genres
        )
        count = len(film_works_ids)
        logger.debug(FINISHED_GETTING_OBJECTS.format(count=count))
        return film_works_ids
