from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
# Create your views here.

class AuthorListView(generics.ListAPIView):
    """
    Read-only endpoint returning authors with nested books for quick verification.
    """
    queryset = Author.objects.prefetch_related("books")
    serializer_class = AuthorSerializer


class BookListView(generics.ListAPIView):
    """
    Read-only endpoint returning books to verify validation and fields.
    """
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
