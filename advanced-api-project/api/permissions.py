from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Read-only access (GET, HEAD, OPTIONS) is allowed for any user.
    - Write access (POST, PUT, PATCH, DELETE) is restricted to authenticated admin users.
    """

    def has_permission(self, request, view):
        # Allow safe methods for everyone
        if request.method in SAFE_METHODS:
            return True
        # Only allow write methods if user is authenticated and is staff/admin
        return request.user and request.user.is_authenticated and request.user.is_staff
