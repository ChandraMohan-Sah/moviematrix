from django.db import models
from django.conf import settings  # for user model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from app1_media_manger.models import MovieMedia
from app2_gener_platform.models import Genre, Platform
from app8_lang_prod_company.models import Language, ProductionCompany
from app3_cast.models import Cast
from app4_creator.models import Creator 
from app5_writer.models import Writer

 
'''
    Notes:
        - duration : This movie is 120 minutes long.
        - runtime : Runtime without intermission is 117 minutes.

    Notes : 
        - ForeignKey: One-to-many relationship
            Example: One movie has many reviews.

        - OneToOne: One-to-one relationship (unique)
            Example: One movie has one core detail.

        - ManyToMany: Many-to-many relationship
            Example: A movie has many production companies, and a company works on many movies. 
'''


class Movie(models.Model):
    """Main movie model in app6 with media integration"""
    moviemedia = models.OneToOneField(
        MovieMedia,
        on_delete=models.CASCADE,
        related_name='app6_movie'
    )
    
    # Media access shortcut
    @property
    def title(self):
        return self.moviemedia.name
    
    @property
    def trailer(self):
        return self.moviemedia.media_files.filter(media_type='trailer')
    
    @property
    def video(self):
        return self.moviemedia.media_files.filter(media_type='video')

    @property
    def banners(self):
        return self.moviemedia.media_files.filter(media_type='banner')
    
    @property
    def thumbnails(self):
        return self.moviemedia.media_files.filter(media_type='thumbnail')
    
    @property
    def related_pic(self):
        return self.moviemedia.media_files.filter(media_type='related_pic')

    movie_genre = models.ManyToManyField(Genre,  related_name='movie_genre')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="movie_released_platform")

    movie_cast = models.ManyToManyField(Cast, related_name='movie_cast')
    movie_creator = models.ManyToManyField(Creator, related_name="movie_creator")
    movie_writer = models.ManyToManyField(Writer, related_name="movie_writer")

    movie_created = models.DateTimeField(auto_now_add=True)
    movie_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} - created at : ({self.movie_created} | updated at : {self.movie_updated})"


class MovieGeneralDetail(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='movie_general_detail')
    active = models.BooleanField()
    is_original = models.BooleanField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    storyline = models.TextField()

    def __str__(self):
        return f"{self.movie} with length {self.duration } is {self.active}."


class MovieRatingReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name='movie_reviews')
    user_movie_review = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_movie_review')
    rating = models.PositiveIntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)])
    review = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Movie: {self.movie.title} has - Rating: {self.rating}"
    

class MovieCoreDetail(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name="movie_core_detail")
    release_date = models.DateField()
    country_of_origin = models.CharField(max_length=100)
    also_known_as = models.CharField(max_length=255, blank=True)
    filming_location = models.CharField(max_length=255, blank=True)

    language = models.ManyToManyField(Language, related_name='movie_language')
    production_companies = models.ManyToManyField(ProductionCompany, related_name='movie_prod_company')

    def __str__(self):
        return f"Core Detail: {self.movie.title}"


class MovieBoxOffice(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name="movie_box_office")
    budget = models.BigIntegerField(help_text="Budget in USD (e.g., 150000000)")
    gross_country = models.BigIntegerField(help_text="Total gross in country of origin (USD)")
    opening_weekend = models.BigIntegerField(help_text="Opening weekend earnings (USD)")
    gross_worldwide = models.BigIntegerField(help_text="Total worldwide gross (USD)")

    def __str__(self):
        return f"Box Office Collection for movie :  {self.movie.title}"


class MovieTechSpecs(models.Model):
    COLOR_CHOICES = [
        ('color', 'Color'),
        ('bw', 'Black and White'),
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

    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name="movie_tech_specs")
    runtime = models.PositiveIntegerField(help_text="Runtime in minutes")
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='color')
    sound_mix = models.CharField(max_length=30, choices=SOUND_MIX_CHOICES, default='dolby_atmos')

    def __str__(self):
        return f"Tech Specification for: {self.movie.title}."


class UserMovieWatchlist(models.Model):
    user_watchlist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_watchlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_watchlist', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user_watchlist.username} watchlisted {self.movie.title}" 


class UserMovieViewed(models.Model):
    user_viewed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='viewed_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='viewed_by')
    viewed_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(auto_now=True)

    class Meta: 
        unique_together = ('user_viewed', 'movie')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user_viewed.username} viewed {self.movie.title}"
    

class MovieVotes(models.Model):
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
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="votes")
    vote_type = models.CharField(max_length=20, choices = VOTE_CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_vote', 'movie')  # 1 vote per user per movie

    def __str__(self):
        return f"{self.user_vote.username} voted '{self.vote_type}' for {self.movie.title}"

class MovieWatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_watch_history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watch_history')
    watched_at = models.DateTimeField(auto_now_add=True)
    duration_watched = models.PositiveIntegerField(null=True, blank=True, help_text="Duration watched in seconds")
    is_completed = models.BooleanField(default=False, help_text="Whether the movie was fully watched")

    class Meta:
        ordering = ['-watched_at']  # Latest first
        unique_together = ('user', 'movie', 'watched_at')  # Prevent duplicate entries at same timestamp

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title} at {self.watched_at}" 

 