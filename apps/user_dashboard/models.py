from django.db import models
from django.contrib.auth.models import User 
from user_profile.models import UserProfile

class UserDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard')

    # helper properties 
    @property
    def profile(self):
        return self.user.profile 

    # ------------------Movie Information ----------------
    @property
    def movie_watchlist(self):
        return self.user.movie_watchlist.all()

    @property
    def movie_ratings_reviews(self):
        return self.user.user_movie_review.all()

    @property
    def movie_viewed(self):
        return self.user.viewed_movies.all()

    
    # ------------------TvShow Information -------------------

    @property 
    def tvshow_watchlist(self):
        return self.user.tvshow_watchlist.all()
    
    
    @property 
    def tvshow_rating_reviews(self):
        return self.user.user_tvshow_review.all()

    @property 
    def tvshow_viewed(self):
        return self.user.viewed_tvshow.all()


    # ------------------Episode Iepisode_watchlistnformation -------------------
    @property 
    def episode_watchlist(self):
        return self.user.episode_watchlist.all() 

    @property 
    def episode_rating_reviews(self):
        return self.user.user_episode_review.all()

    @property 
    def episode_viewed(self):
        return self.user.episode_viewed.all()  


    # --------------------Watch History ------------------------
    @property
    def movie_watch_history(self):
        return self.user.movie_watch_history.all()

    def __str__(self):
        return f"{self.user.username}'s Dashboard"
    
 