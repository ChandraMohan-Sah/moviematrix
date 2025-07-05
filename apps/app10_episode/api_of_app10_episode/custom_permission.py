from rest_framework import permissions

class IsEpisodeReviewer_OrReadOnly(permissions.BasePermission):
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
            return obj.user_episode_review == request.user
    


class IsEpisodeVoter_OrReadOnly(permissions.BasePermission):
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
            # Allow write methods only for the user who voted
            return obj.user_vote == request.user
    


class IsUserEpisodeWatchlist_OrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        else:
            # Allow write methods only for the user who watchlisted
            return obj.user_watchlist == request.user



    
class IsAdminOrUserWatchlistedEpisode(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return obj.user_watchlist == request.user  # Allow read-only methods to the user who watchlisted 
        
        else:
            # Check permissions for write request
            return obj.user_watchlist == request.user or request.user.is_staff # Allow write methods : for admin + particular users
    



class IsUserViewedEpisode_OrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        else:
            # Allow write methods only for the user who viewed the review
            return obj.user_viewed == request.user
    

class IsAdminOrUserViewedEpisode(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return obj.user_viewed == request.user # Allow read-only methods for the user who viewed
        
        else:
            # Check permissions for write request
            return obj.user_viewed ==  request.user or request.user.is_staff  # Allow write methods : for admin + particular users
    
