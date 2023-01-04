import logging
import uuid

from typing import List
from django.db import connection


from etl.servises.defines import MOVIES
from movies.models import Person, FilmWork

logger = logging.getLogger("logger")


class Transformer:
    def __init__(self, film_work_ids):
        self.film_work_ids: List[uuid.UUID] = tuple(film_work_ids)
        self.film_works_list: List[FilmWork] = list()

    @staticmethod
    def _person_to_dict(person: Person):
        return {
            "id": str(person.id),
            "name": person.full_name,
        }

    def _film_work_to_dict(self):
        sql = (
            "SELECT "
            "fw.id::text, "
            "fw.rating as imdb_rating, "
            "COALESCE (json_agg(DISTINCT g.name) "
            "FILTER (WHERE g.id is not null)) "
            "as genre, "
            "fw.title, "
            "fw.description, "
            "COALESCE (json_agg(DISTINCT p.full_name)"
            " FILTER (WHERE p.id is not null and "
            "pfw.role = 'director'), '[]') "
            "as director, "
            "COALESCE (json_agg(DISTINCT p.full_name) "
            "FILTER (WHERE p.id is not null and pfw.role = 'actor')) "
            "as actors_names, "
            "COALESCE (json_agg(DISTINCT p.full_name) "
            "FILTER (WHERE p.id is not null and pfw.role = 'writer')) "
            "as writers_names, "
            "COALESCE (json_agg(DISTINCT jsonb_build_object("
            "'id', p.id,"
            "'name', p.full_name"
            ")) FILTER (WHERE p.id is not null and pfw.role = 'actor')) "
            "as actors, "
            "COALESCE (json_agg(DISTINCT jsonb_build_object("
            "'id', p.id,"
            "'name', p.full_name"
            ")) FILTER (WHERE p.id is not null and "
            "pfw.role = 'writer')) "
            "as writers "
            "FROM content.film_work fw "
            "LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = "
            "fw.id "
            "LEFT JOIN content.person p ON p.id = pfw.person_id "
            "LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = "
            "fw.id "
            "LEFT JOIN content.genre g ON g.id = gfw.genre_id "
            "WHERE fw.id in %s "
            "GROUP BY fw.id "
            "ORDER BY fw.modified; "
        )
        with connection.cursor() as cursor:
            cursor.execute(sql, [self.film_work_ids])
            columns = [col[0] for col in cursor.description]
            cursor = cursor.fetchall()
            rows = [dict(zip(columns, row)) for row in cursor]
        return rows

    def film_work_to_list_of_dict(self):
        logger.debug("Start transformation objects for updating")
        data_list = self._film_work_to_dict()
        for obj in data_list:
            self.film_works_list.append(
                {
                    "_index": MOVIES,
                    "_id": obj["id"],
                    "_source": obj,
                }
            )
        logger.debug("End transformation objects for updating")
        return self.film_works_list
