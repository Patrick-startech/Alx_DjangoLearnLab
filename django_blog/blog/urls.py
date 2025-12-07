# blog/urls.py
from django.urls import path
from .views import (
    # Post views
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,

    # Auth views
    index, BlogLoginView, BlogLogoutView, register, profile,

    # Comment views
    CommentCreateView, CommentUpdateView, CommentDeleteView,

    # Tag & Search views
    TagPostListView, SearchResultsView,
)

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),

    # Auth
    path('login/', BlogLoginView.as_view(), name='login'),
    path('logout/', BlogLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    # Posts CRUD
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Comments CRUD
    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Tags & Search
    path('tags/<slug:slug>/', TagPostListView.as_view(), name='tag_posts'),
    path('search/', SearchResultsView.as_view(), name='search'),
]
