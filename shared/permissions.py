from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
        Custom permission to only allow admin users to edit objects.
        Non-admin users can only read objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True  # Allow read-only methods for all users
        
        else:
            # Check permissions for write request
            return request.user and request.user.is_staff  # Allow write methods only for admin users
    

 