from rest_framework import permissions

class IsTVShowReviewer_OrReadOnly(permissions.BasePermission):
    """
        Custom permission to only allow the user who created the review to edit it.
        Other users can only read the review.
        
        - SAFE_METHODS (GET, HEAD, OPTIONS): allow anyone.
        - Other methods (PUT, PATCH, DELETE): only the reviewer (owner) is allowed.

    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        else:
            # Allow write methods only for the user who created the review
            # print(dir(obj))
            # print(obj.user_tvshow_review)
            return obj.user_tvshow_review == request.user
    


class IsTvShowVoter_OrReadOnly(permissions.BasePermission):
    """
        Custom permission to only allow the user who created the review to edit it.
        Other users can only read the review.
        
        - SAFE_METHODS (GET, HEAD, OPTIONS): allow anyone.
        - Other methods (PUT, PATCH, DELETE): only the reviewer (owner) is allowed.

    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        else:
            # Allow write methods only for the user who created the review
            return obj.user_vote == request.user
    


class IsUserTvShowWatchlist_OrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        else:
            # Allow write methods only for the user who created the review
            return obj.user_watchlist == request.user



    
class IsAdminOrUserWatchlistedTvShow(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True  # Allow read-only methods for all users
        
        else:
            # Check permissions for write request
            return request.user_watchlist and request.user.is_staff  # Allow write methods only for admin users
    



class IsUserViewedTvshow_OrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        else:
            # Allow write methods only for the user who created the review
            return obj.user_viewed == request.user
    

class IsAdminOrUserViewedTvShow(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True  # Allow read-only methods for all users
        
        else:
            # Check permissions for write request
            return request.user_viewed and request.user.is_staff  # Allow write methods only for admin users
    
