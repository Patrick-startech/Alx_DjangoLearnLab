from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# -----------------------------
# Author Views
# -----------------------------
class AuthorListView(generics.ListAPIView):
    """
    Read-only endpoint returning authors with nested books.
    Accessible to everyone.
    """
    queryset = Author.objects.prefetch_related("books")
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# Book Views (CRUD + Filtering/Search/Ordering)
# -----------------------------
class BookListView(generics.ListAPIView):
    """
    List all books with filtering, searching, and ordering.
    - Filtering: title, author (id), publication_year
    - Searching: partial text on title and author name
    - Ordering: title, publication_year
    Accessible to everyone.
    """
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Enable filter/search/order backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering by exact field values
    filterset_fields = ["title", "author", "publication_year"]

    # Searching across text fields (case-insensitive contains)
    search_fields = ["title", "author__name"]

    # Allow client to order results by chosen fields
    ordering_fields = ["title", "publication_year", "id"]
    ordering = ["title"]  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID.
    Accessible to everyone.
    """
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic can be added here (e.g., attach request.user if needed)
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        # Custom logic for updates (e.g., audit logging)
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


# -----------------------------
# Homepage
# -----------------------------
# Simple homepage view for the root URL.
# Returns a JSON message confirming the API is running.

def home(request):
    return JsonResponse({
        "message": "Welcome to the Advanced API Project!",
        "method": request.method,  # now request is accessed
        "user": str(request.user) if request.user.is_authenticated else "Anonymous",
        "endpoints": {
            "authors": "/api/authors/",
            "books": "/api/books/",
            "book detail": "/api/books/<id>/",
            "book create": "/api/books/create/",
            "book update": "/api/books/<id>/update/",
            "book delete": "/api/books/<id>/delete/"
        }
    })



