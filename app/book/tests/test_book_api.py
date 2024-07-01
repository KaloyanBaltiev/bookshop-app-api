"""
Tests for book app.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Book,
    Author,
)

from book.serializers import (
    BookSerializer,
    AuthorSerializer
)


BOOKS_URL = reverse('book:book-list')


def detail_url(book_id):
    """Create and return a book detail URL."""
    return reverse('book:book-detail', args=[book_id])


def create_author(**params):
    """Create and return author entry."""
    defaults = {
        'first_name': 'John',
        'last_name': 'Dough',
        'nationality': "USA",
        'years_old': 33,
        'gender': Author.Gender.MALE,
    }
    defaults.update(params)
    author = Author.objects.create(**defaults)
    return author


def create_book(**params):
    """Create and return book entry."""
    author = params.pop('author', None)
    if author:
        author_obj, _ = Author.objects.get_or_create(**author)
    else:
        author_obj = create_author()
    defaults = {
        'author': author_obj,
        'title': 'Simple Book',
        'year_of_publicity': 1987,
        'covers': Book.Type.SOFT,
        'language': Book.Language.EN,
        'genre': Book.Genre.FANTASY,
        'pages': 100,
    }
    defaults.update(params)
    book = Book.objects.create(**defaults)
    return book


class PublicBookAPITests(TestCase):
    """Test API requests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.book = create_book()

    def test_retrieve_books(self):
        response = self.client.get(BOOKS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author']['first_name'], self.book.author.first_name)
        self.assertEqual(response.data[0]['author']['last_name'], self.book.author.last_name)
        self.assertEqual(response.data[0]['title'], self.book.title)
        self.assertEqual(response.data[0]['year_of_publicity'], self.book.year_of_publicity)
        self.assertEqual(response.data[0]['covers'], self.book.covers)
        self.assertEqual(response.data[0]['language'], self.book.language)
        self.assertEqual(response.data[0]['genre'], self.book.genre)
        self.assertEqual(response.data[0]['pages'], self.book.pages)

    def test_create_book(self):
        data = {
            'author':
                {'first_name': 'John', 'last_name': 'Dough'},
            'title': 'new title',
            'year_of_publicity': 1234,
            'covers': 'soft',
            'language': 'Spanish',
            'genre': 'technical',
            'pages': 1234

        }
        response = self.client.post(BOOKS_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_book = Book.objects.all().filter(title=data['title'])
        self.assertTrue(new_book.exists())
        self.assertEqual(data['year_of_publicity'], new_book[0].year_of_publicity)
        self.assertEqual(data['covers'], new_book[0].covers)
        self.assertEqual(data['language'], new_book[0].language)
        self.assertEqual(data['genre'], new_book[0].genre)
        self.assertEqual(data['pages'], new_book[0].pages)

    def test_update_book(self):
        data = {
            'author':
                {'first_name': 'John', 'last_name': 'Dough'},
            'title': 'new title',
            'year_of_publicity': 1234,
            'covers': 'soft',
            'language': 'Spanish',
            'genre': 'technical',
            'pages': 1234

        }
        url = detail_url(self.book.id)
        response = self.client.patch(url, data, format='json')
        self.book.refresh_from_db()
        self.assertEqual(data['title'], self.book.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['year_of_publicity'], self.book.year_of_publicity)
        self.assertEqual(data['covers'], self.book.covers)
        self.assertEqual(data['language'], self.book.language)
        self.assertEqual(data['genre'], self.book.genre)
        self.assertEqual(data['pages'], self.book.pages)

    def test_filter_books(self):
        female_author = {
            'first_name': 'Agata',
            'last_name': 'Christie',
            'nationality': "UK",
            'years_old': 33,
            'gender': Author.Gender.FEMALE,
        }

        book_female_author = create_book(author=female_author)

        res = self.client.get(BOOKS_URL, {'number_of_pages': '1', 'author_gender': 'female'})

        b1 = BookSerializer(book_female_author)
        b2 = BookSerializer(self.book)
        self.assertIn(b1.data, res.data)
        self.assertNotIn(b2.data, res.data)
