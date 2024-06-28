"""
Views for the recipes APIs.
"""
from rest_framework import viewsets
from core.models import (
    Author,
    Book,
)
from book import serializers


class BookViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()

    def get_queryset(self):
        """Filter queryset"""
        pages = int(self.request.query_params.get('number_of_pages'))
        gender = self.request.query_params.get('author_gender')
        queryset = self.queryset
        queryset = queryset.filter(pages__gt=pages, author__gender=gender)
        return queryset
