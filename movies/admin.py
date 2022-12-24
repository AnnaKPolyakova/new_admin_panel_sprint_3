from django.contrib import admin

from movies.models import (FilmWork, Genre, GenreFilmWork, Person,
                           PersonFilmWork)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("film_work", "person")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created")
    list_filter = ("full_name",)
    search_fields = ("full_name",)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    list_display = (
        "film_work",
        "genre",
        "created",
    )
    list_filter = ("genre", "created")
    search_fields = ("genre", "film_work", "created")
    autocomplete_fields = ("genre",)


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    list_display = (
        "film_work",
        "genre",
        "creation_date",
        "created",
    )
    list_filter = ("genre", "created")
    search_fields = (
        "film_work",
        "created",
        "person",
    )
    autocomplete_fields = ("person",)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = ("type",)
    search_fields = ("title", "description", "id")
