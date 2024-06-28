"""
Serializers for Book APIs.
"""
from rest_framework import serializers

from core.models import (
    Book,
    Author,
)


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author."""

    class Meta:
        model = Author
        fields = ['id', 'first_name',
                  'last_name']  # TODO: FE should be going to a different endpoint creating an author
        read_only_fields = ['id']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book."""

    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'author', 'title', 'year_of_publicity',
                  'covers', 'language', 'genre', 'pages']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Add a book."""
        author = validated_data.pop('author', None)
        if author:
            author_obj, created = Author.objects.get_or_create(**author)
            validated_data["author_id"] = author_obj.id
            book = Book.objects.create(**validated_data)
            return book

    def update(self, instance, validated_data):
        """Update a Book."""
        author = validated_data.pop('author', None)
        if author:
            author_obj, created = Author.objects.get_or_create(**author)
            validated_data["author_id"] = author_obj.id
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
