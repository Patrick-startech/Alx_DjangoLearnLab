from django.urls import path
from .views import AuthorListView, BookListView

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('books/', BookListView.as_view(), name='book-list'),
]
