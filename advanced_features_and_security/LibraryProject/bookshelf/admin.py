from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser  # Import both models

# Book Admin (existing)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
    list_display_links = ('title',)

admin.site.register(Book, BookAdmin)

# CustomUser Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add custom fields to admin forms
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth']

admin.site.register(CustomUser, CustomUserAdmin)