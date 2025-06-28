from django.db import models

from app1_media_manger.models import EpisodeMedia
from django.conf import settings 
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator


class Episode(models.Model):
    """Main episode model in app9 with media integration"""
    episodemedia = models.OneToOneField(
        EpisodeMedia, 
        on_delete=models.CASCADE,
        related_name='app10_episode'
    ) 
 
    @property 
    def episode_title(self): 
        return self.episodemedia.title 
    
    @property 
    def tvshow(self):
        return self.episodemedia.tvshow.name 
    
    @property
    def season(self):
        return self.episodemedia.season.season_number 
    
    @property
    def episode_number(self):
        return self.episodemedia.episode_number 
    
    @property
    def thumbnails(self):
        return self.episodemedia.media_files.filter(media_type='thumbnail')  
    
    @property
    def videos(self):
        return self.episodemedia.media_files.filter(media_type='video')
    
    

    '''
        - Director , Writer , Cast -> fetch from app7 and show to frontent
        - tech specs, core detail -> fetch from app7 and show to frontent 
        - genre, platform  all 

    '''
    episode_created = models.DateTimeField(auto_now_add=True)
    episode_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Episode : {self.episode_title} from tvshow {self.tvshow} and season {self.season}"


 

class EpisodeGeneralDetail(models.Model):
    episode = models.OneToOneField(Episode, on_delete=models.CASCADE, related_name='episode_general_detail')
    active = models.BooleanField()
    is_original = models.BooleanField() 
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    storyline = models.TextField()

    def __str__(self):
        return f"{self.episode} with average rating {self.avg_rating} is {self.active}"
    
 


class EpisodeWatchlist(models.Model):
    user_watchlist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="episode_watchlisted_by")

    added_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(auto_now=True)

    class Meta: 
        unique_together = ('user_watchlist', 'episode')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user_watchlist.username} watchlisted episode {self.episode.episode_title}"
    



class EpisodeViewed(models.Model):
    user_viewed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="episode_viewed_by")

    viewed_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(auto_now=True)

    class Meta: 
        unique_together = ('user_viewed', 'episode')
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user_viewed.username} viewed episode {self.episode.episode_title}"
    



class EpisodeVotes(models.Model):
    VOTE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('love', 'Love'),
        ('appreciate', 'Appreciate'),
        ('insightful', 'Insightful'),
        ('funny', 'Funny'),
        ('excited', 'Excited'),
    ]

    user_vote = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="episode_votes")
    vote_type = models.CharField(max_length=20, choices = VOTE_CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_vote', 'episode')  # 1 vote per user per episode

    def __str__(self):
        return f"{self.user_vote.username} voted '{self.vote_type}' for {self.episode.episode_title}"


class EpisodeRatingReview(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="episode_reviews")
    user_episode_review = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_episode_review" )
    rating = models.PositiveIntegerField(validators= [MinValueValidator(1), MaxValueValidator(10)])
    review = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Episode : {self.episode.episode_title} has - Rating: {self.rating}"


