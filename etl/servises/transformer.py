import logging

from etl.servises.defines import MOVIES
from movies.models import Person

logger = logging.getLogger("logger")


class Transformer:
    def __init__(self, film_work_qs):
        self.film_work_qs = film_work_qs
        self.film_works_list = list()

    @staticmethod
    def _person_to_dict(person: Person):
        return {
            "id": str(person.id),
            "name": person.full_name,
        }

    def _film_work_to_dict(self, obj):
        return {
            "id": str(obj.id),
            "imdb_rating": obj.rating,
            "genre": [str(genre.name) for genre in obj.genres.all()],
            "title": obj.title,
            "description": obj.description,
            "director": [
                str(person.full_name) for person in obj.persons.filter(
                    person_film_work__role='director'
                )
            ],
            "actors_names": [
                str(person.full_name) for person in obj.persons.filter(
                    person_film_work__role='actor'
                )
            ],
            "writers_names": [
                str(person.full_name) for person in obj.persons.filter(
                    person_film_work__role='writer'
                )
            ],
            "actors": [
                self._person_to_dict(person) for person in obj.persons.filter(
                    person_film_work__role='actor'
                )
            ],
            "writers": [
                self._person_to_dict(person) for person in
                obj.persons.filter(person_film_work__role='writer')
            ],
        }

    def film_work_to_list_of_dict(self):
        logger.debug("Start transformation objects for updating")
        for obj in self.film_work_qs:
            self.film_works_list.append(
                {
                    '_index': MOVIES,
                    '_id': str(obj.id),
                    '_source': self._film_work_to_dict(obj)
                }
            )
        logger.debug("End transformation objects for updating")
        return self.film_works_list
