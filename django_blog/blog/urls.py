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
    path('post/new/', PostCreateView.as_view(), name='post_create'),              # <-- updated
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),  # <-- updated
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    
        # Comments CRUD
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),


    # Tags & Search
    path('tag/<slug:slug>/', TagPostListView.as_view(), name='tag_posts'),
    path('search/', SearchResultsView.as_view(), name='search'),
]
