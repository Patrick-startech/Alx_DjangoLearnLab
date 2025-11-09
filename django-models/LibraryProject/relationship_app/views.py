from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()  # Required for milestone check
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Required for milestone check
    context_object_name = 'library'
