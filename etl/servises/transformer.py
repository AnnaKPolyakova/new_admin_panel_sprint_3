from typing import List

from movies.models import FilmWork, Person


def person_to_dict(person: Person):
    return {
        "id": str(person.id),
        "name": person.full_name,
    }


def film_work_to_dict(queryset: List[FilmWork]):
    film_works_dict = list()
    for obj in queryset:
        film_works_dict.append(
            {
                "id": obj.id,
                "imdb_rating": obj.rating,
                "genre": [str(genre.name) for genre in obj.genres.all()],
                "title": obj.title,
                "description": obj.description,
                "director": [
                    str(person.full_name) for person in obj.persons.filter(
                        role='director'
                    )
                ],
                "actors_names": [
                    str(person.full_name) for person in obj.persons.filter(
                        role='actor'
                    )
                ],
                "writers_names": [
                    str(person.full_name) for person in obj.persons.filter(
                        role='writer'
                    )
                ],
                "actors": [
                    person_to_dict(person) for person in
                    obj.persons.filter(
                        role='actor'
                    )
                ],
                "writers": [
                    person_to_dict(person) for person in
                    obj.persons.filter(
                        role='writer'
                    )
                ],
            }
        )
    return film_works_dict
