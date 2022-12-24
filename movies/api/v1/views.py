from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from config.settings import PAGINATION_SIZE
from movies.models import FilmWork, PersonFilmWork


class PersonsGetQuerySetMixin:
    def get_actors_directors_writers(self):
        actors = PersonFilmWork.objects.filter(
            film_work=OuterRef("pk"), role="actor"
        ).values_list("person__full_name", flat=True)
        directors = PersonFilmWork.objects.filter(
            film_work=OuterRef("pk"), role="director"
        ).values_list("person__full_name", flat=True)
        writers = PersonFilmWork.objects.filter(
            film_work=OuterRef("pk"), role="writer"
        ).values_list("person__full_name", flat=True)
        return actors, directors, writers


class MoviesListApi(BaseListView, PersonsGetQuerySetMixin):
    model = FilmWork
    http_method_names = ["get"]
    paginate_by = int(PAGINATION_SIZE)

    def get_queryset(self):
        actors, directors, writers = self.get_actors_directors_writers()
        return (
            FilmWork.objects.prefetch_related(
                "genres",
                "people",
            )
            .values(
                "id", "title", "description", "creation_date", "rating", "type"
            )
            .annotate(
                genres=ArrayAgg("genres__name", distinct=True),
                actors=ArraySubquery(actors),
                directors=ArraySubquery(directors),
                writers=ArraySubquery(writers),
            )
        )

    def _get_paginate_context(self, queryset):
        paginator, page, queryset, _ = self.paginate_queryset(
            queryset, self.get_paginate_by(queryset)
        )
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous()
            else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        return self._get_paginate_context(queryset)

    def render_to_response(self, context, **response_kwargs):
        if not context:
            return JsonResponse({"result": "not_found"}, status=404)
        return JsonResponse(context)


class MoviesDetailApi(BaseListView, PersonsGetQuerySetMixin):
    model = FilmWork
    http_method_names = ["get"]

    def get_object(self):
        actors, directors, writers = self.get_actors_directors_writers()
        return (
            FilmWork.objects.filter(
                id=self.request.resolver_match.kwargs.get("pk")
            ).values(
                "id", "title", "description", "creation_date", "rating", "type"
            ).annotate(
                genres=ArrayAgg("genres__name", distinct=True),
                actors=ArraySubquery(actors),
                directors=ArraySubquery(directors),
                writers=ArraySubquery(writers),
            )
            .first()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_object()

    def render_to_response(self, context, **response_kwargs):
        if not context:
            return JsonResponse({"result": "not_found"}, status=404)
        return JsonResponse(context)
