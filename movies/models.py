import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created"),
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_("modified"),
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("description"),
    )

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")

    full_name = models.CharField(
        max_length=255,
        verbose_name=_("full_name"),
    )
    gender = models.TextField(
        choices=Gender.choices,
        null=True,
        verbose_name=_("gender"),
        blank=True,
    )

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmWorkType(models.TextChoices):
        ART_DIRECTION = "movie", _("movie")
        FESTIVAL_TEAM = "tv_show", _("tv_show")

    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
        null=True,
    )
    creation_date = models.DateTimeField(
        verbose_name=_("creation_date"),
        null=True,
    )
    rating = models.FloatField(
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("rating"),
    )
    type = models.CharField(
        choices=FilmWorkType.choices,
        max_length=50,
        verbose_name=_("type"),
    )
    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmWork",
        related_name="film_work",
        verbose_name=_("genres"),
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmWork",
        related_name="film_work",
        verbose_name=_("persons"),
    )
    certificate = models.CharField(
        max_length=512,
        blank=True,
        verbose_name=_("certificate"),
    )
    file_path = models.FileField(
        blank=True,
        null=True,
        upload_to="movies/",
        verbose_name=_("file"),
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film work")
        verbose_name_plural = _("Film works")

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name="genre_film_work",
        verbose_name=_("film_work"),
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name="genre_film_work",
        verbose_name=_("genre")
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created"),
    )

    class Meta:
        db_table = 'content"."genre_film_work'


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name="person_film_work",
        verbose_name=_("film_work"),
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="person_film_work",
        verbose_name=_("person"),
    )
    role = models.CharField(
        max_length=255,
        null=True,
        verbose_name=_("role"),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created"),
    )

    class Meta:
        db_table = 'content"."person_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="film_work_person_role_idx",
            )
        ]
