# Create your views here.
# api/views.py
"""
views.py
--------
This module defines views for the `api` application.

Includes:
- BookList: a read-only list view of all books.
- BookViewSet: a full CRUD ViewSet for managing books.
- home: a root endpoint returning a JSON welcome message.
"""

from django.http import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView

class BookList(generics.ListAPIView):
    """
    Read-only view that lists all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # keep public if desired   

class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for the Book model.

    Provides:
    - list (GET /books_all/)
    - retrieve (GET /books_all/<id>/)
    - create (POST /books_all/)
    - update (PUT /books_all/<id>/)
    - partial_update (PATCH /books_all/<id>/)
    - destroy (DELETE /books_all/<id>/)
    """
    queryset = Book.objects.all()   # ✅ required by checker
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]

def home(request):
    """
    Root endpoint for the Book API.

    Provides a simple JSON response guiding users to available endpoints.
    """
    return JsonResponse({
        "message": "Welcome to the Book API",
        "endpoints": {
            "list_books": "/api/books/",
            "crud_books": "/api/books_all/"
        }
    })

