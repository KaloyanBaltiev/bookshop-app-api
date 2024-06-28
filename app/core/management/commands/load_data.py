"""
Django command for loading data to db
"""
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Author, Book


class Command(BaseCommand):
    """Load data from an Excel file into the database"""

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        data = pd.read_excel(file_path)

        for _, row in data.iterrows():
            author, created = Author.objects.get_or_create(
                first_name=row['author_first_name'],
                last_name=row['author_last_name'],
                nationality=row['author nationality'],
                years_old=row['author years old'],
                gender=Author.Gender(row['author gender'])
            )
            Book.objects.get_or_create(
                author=author,
                title=row['book name'],
                year_of_publicity=row['year of publicity'],
                covers=Book.Type(row['covers']),
                language=Book.Language(row['language']),
                genre=Book.Genre(row['genre']),
                pages=row['pages'],
            )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
