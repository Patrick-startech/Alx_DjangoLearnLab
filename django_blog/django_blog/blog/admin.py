from django.contrib import admin
from .models import Post, Profile, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for blog posts."""
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('published_date', 'author')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for user profiles."""
    list_display = ('user', 'bio', 'avatar')
    search_fields = ('user__username', 'user__email', 'bio')
    list_filter = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for comments."""
    list_display = ('post', 'author', 'created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'post__title')
    list_filter = ('created_at', 'author')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
