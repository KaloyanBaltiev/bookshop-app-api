"""
Database models.
"""
from django.db import models


class Author(models.Model):
    """Author object."""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255, null=True)
    # TODO: Find the actual date of birth, was not provided in the data
    years_old = models.PositiveSmallIntegerField(null=True)

    class Gender(models.TextChoices):
        MALE = "male", "male"
        FEMALE = "female", "female"
    gender = models.CharField(max_length=6, choices=Gender.choices, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Book(models.Model):
    """Book object."""
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )
    title = models.TextField()
    year_of_publicity = models.PositiveSmallIntegerField()

    class Type(models.TextChoices):
        SOFT = "soft", "soft"
        HARD = "hard", "hard"
        DIGITAL = "digital", "digital"

    covers = models.CharField(max_length=255, choices=Type.choices)

    class Language(models.TextChoices):
        EN = "English"
        DE = "German"
        BG = "Bulgarian"
        ES = "Spanish"

    language = models.CharField(
        max_length=255, choices=Language.choices
    )

    class Genre(models.TextChoices):
        TECHNICAL = "technical", "Technical"
        FANTASY = "Fantasy", "Fantasy"
        HORROR = "Horror", "Horror"

    genre = models.TextField(max_length=255, choices=Genre.choices)

    pages = models.PositiveIntegerField()

    def __str__(self):
        return self.title
