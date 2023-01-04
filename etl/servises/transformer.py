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
        sql = f'SELECT ' \
              f'fw.id::text, ' \
              f'fw.rating as imdb_rating, ' \
              f'COALESCE (json_agg(DISTINCT g.name) ' \
              f'FILTER (WHERE g.id is not null)) ' \
              f'as genre, ' \
              f'fw.title, ' \
              f'fw.description, ' \
              f'COALESCE (json_agg(DISTINCT p.full_name)' \
              f' FILTER (WHERE p.id is not null and ' \
              f'pfw.role = \'director\'), \'[]\') ' \
              f'as director, ' \
              f'COALESCE (json_agg(DISTINCT p.full_name) ' \
              f'FILTER (WHERE p.id is not null and pfw.role = \'actor\')) ' \
              f'as actors_names, ' \
              f'COALESCE (json_agg(DISTINCT p.full_name) ' \
              f'FILTER (WHERE p.id is not null and pfw.role = \'writer\')) ' \
              f'as writers_names, ' \
              f'COALESCE (json_agg(DISTINCT jsonb_build_object(' \
              f'\'id\', p.id,' \
              f'\'name\', p.full_name' \
              f')) FILTER (WHERE p.id is not null and pfw.role = \'actor\')) ' \
              f'as actors, ' \
              f'COALESCE (json_agg(DISTINCT jsonb_build_object(' \
              f'\'id\', p.id,' \
              f'\'name\', p.full_name' \
              f')) FILTER (WHERE p.id is not null and ' \
              f'pfw.role = \'writer\')) ' \
              f'as writers ' \
              f'FROM content.film_work fw ' \
              f'LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = ' \
              f'fw.id ' \
              f'LEFT JOIN content.person p ON p.id = pfw.person_id ' \
              f'LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = ' \
              f'fw.id ' \
              f'LEFT JOIN content.genre g ON g.id = gfw.genre_id ' \
              f'WHERE fw.id in %s ' \
              f'GROUP BY fw.id ' \
              f'ORDER BY fw.modified; ' \

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
