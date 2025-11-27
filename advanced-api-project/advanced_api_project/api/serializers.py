from datetime import date
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of Book:
    - title
    - publication_year
    - author (FK id by default)
    Includes custom validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value):
        # Prevent future years relative to current calendar year
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author with nested books:
    - name: author name
    - books: nested BookSerializer sourced from Author.books (related_name)
    Demonstrates handling of nested relationships via DRF.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
