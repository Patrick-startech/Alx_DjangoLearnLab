from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import generics
from .models import Book
from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # adjust to IsAuthenticated if needed
from .serializers import BookSerializer
from django.http import JsonResponse

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Existing ListAPIView (kept)
from rest_framework.generics import ListAPIView

class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

# New ViewSet for full CRUD
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, partial_update, destroy on Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    # Optional: override for search/filter/order later, or set default ordering
    # def get_queryset(self):
    #     return Book.objects.all().order_by("-id")

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