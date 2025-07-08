from django.db import models
from app1_media_manger.models import TVShowMedia

from app2_gener_platform.models import Genre, Platform
from app3_cast.models import Cast 
from app4_creator.models import Creator 
from app5_writer.models import Writer
from app8_lang_prod_company.models import Language, ProductionCompany

from django.conf import settings  # for user model
from django.contrib.auth.models import User # gives custom user selection

from django.core.validators import MinValueValidator, MaxValueValidator
 
 

# Create your models here.
class TvShow(models.Model):
    """Main tvshow model in app7 with media integration"""
    tvshowmedia = models.OneToOneField(
        TVShowMedia,
        on_delete=models.CASCADE,
        related_name='app7_tvshow' 
    ) 

    @property
    def title(self):
        return self.tvshowmedia.name
    
    @property 
    def banners(self):
        return self.tvshowmedia.media_files.filter(media_type='banner')
    
    @property
    def thumbnails(self):
        return self.tvshowmedia.media_files.filter(media_type='thumbnail')
    
    @property
    def trailers(self):
        return self.tvshowmedia.media_files.filter(media_type='trailer')

    @property 
    def related_pic(self):
        return self.tvshowmedia.media_files.filter(media_type='related_pic')
    

    tvshow_genre = models.ManyToManyField(Genre,  related_name='tvshow_genre')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="tvshow_released_platform")

    tvshow_cast = models.ManyToManyField(Cast, related_name='tvshow_cast')
    tvshow_creator = models.ManyToManyField(Creator, related_name="tvshow_creator")
    tvshow_writer = models.ManyToManyField(Writer, related_name="tvshow_writer")

    tvshow_created = models.DateTimeField(auto_now_add=True)
    tvshow_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} - created at : ({self.tvshow_created} | updated at : {self.tvshow_updated})"



class TvShowGeneralDetail(models.Model):
    tvshow = models.OneToOneField(TvShow, on_delete=models.CASCADE, related_name='tvshow_general_detail')
    active = models.BooleanField()
    is_original = models.BooleanField() 
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    storyline = models.TextField()

    def __str__(self):
        return f"{self.tvshow} with average rating {self.avg_rating} is {self.active}"
    


class TvShowCoreDetail(models.Model):
    tvshow = models.OneToOneField(TvShow, on_delete=models.CASCADE, related_name="tvshow_core_detail")
    release_date = models.DateField()
    country_of_origin = models.CharField(max_length=100)
    also_known_as = models.CharField(max_length=255, blank=True)
    filming_location = models.CharField(max_length=255, blank=True) 

    language = models.ManyToManyField(Language,related_name="tvshow_language")
    production_companies = models.ManyToManyField(ProductionCompany, related_name="tvshow_prod_company")

    def __str__(self):
        return f"Core Detail: {self.tvshow.title}"
    

class TvShowTechSpecs(models.Model):
    COLOR_CHOICES = [
        ('color', 'Color'),
        ('bw', 'Black and White')
    ]

    SOUND_MIX_CHOICES = [
        ('mono', 'Mono'),
        ('stereo', 'Stereo'),
        ('dolby_digital', 'Dolby Digital'),
        ('dts', 'DTS'),
        ('dolby_atmos', 'Dolby Atmos'),
        ('sdds', 'SDDS'),
        ('auro_3d', 'Auro 3D'),
        ('imax_6_track', 'IMAX 6-Track'),      
    ] 

    tvshow = models.OneToOneField(TvShow, on_delete=models.CASCADE, related_name="tvshow_tech_specs")
    runtime = models.PositiveIntegerField(help_text = "Runtime in minutes")
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, default='color')
    sound_mix = models.CharField(max_length=30, choices=SOUND_MIX_CHOICES, default='dolby_atmos')

    def __str__(self):
        return f"Tech Specification for : {self.tvshow.title}"


class UserTvShowWatchlist(models.Model):
    user_watchlist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tvshow_watchlist')
    tvshow = models.ForeignKey(TvShow, on_delete=models.CASCADE, related_name='tvshow_watchlisted_by')

    added_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_watchlist', 'tvshow')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user_watchlist.username} watchlisted {self.tvshow.title}" 


class UserTvShowViewed(models.Model):
    user_viewed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='viewed_tvshow')
    tvshow = models.ForeignKey(TvShow, on_delete=models.CASCADE, related_name='tvshow_viewed_by')
    viewed_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(auto_now=True)

    class Meta: 
        unique_together = ('user_viewed', 'tvshow')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user_viewed.username} viewed {self.tvshow.title}"
    

class TvShowVotes(models.Model):
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
    tvshow = models.ForeignKey(TvShow, on_delete=models.CASCADE, related_name="tvshow_votes")
    vote_type = models.CharField(max_length=20, choices = VOTE_CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_vote', 'tvshow')  # 1 vote per user per movie

    def __str__(self):
        return f"{self.user_vote.username} voted '{self.vote_type}' for {self.tvshow.title}"



class TvShowRatingReview(models.Model):
    tvshow = models.ForeignKey(TvShow, on_delete=models.CASCADE, related_name="tvshow_reviews")
    user_tvshow_review = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tvshow_review" )
    rating = models.PositiveIntegerField(validators= [MinValueValidator(1), MaxValueValidator(10)])
    review = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TvShow : {self.tvshow.title} has - Rating: {self.rating}"
    

class TvShowWatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tvshow_watch_history')
    tvshow = models.ForeignKey(TvShow, on_delete=models.CASCADE, related_name='watch_history')
    watched_at = models.DateTimeField(auto_now_add=True)
    duration_watched = models.PositiveIntegerField(null=True, blank=True, help_text="Duration watched in seconds")
    is_completed = models.BooleanField(default=False, help_text="Whether the tvshow was fully watched")

    class Meta:
        ordering = ['-watched_at']  # Latest first
        unique_together = ('user', 'tvshow', 'watched_at')  # Prevent duplicate entries at same timestamp

    def __str__(self):
        return f"{self.user.username} watched {self.tvshow.title} at {self.watched_at}" 