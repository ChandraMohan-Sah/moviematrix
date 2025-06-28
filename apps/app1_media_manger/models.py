from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils.text import slugify

 
class CastMedia(models.Model):
    name = models.CharField(max_length=255)
    media_files = GenericRelation('MediaFile')  

    def __str__(self):
        return self.name

 
class CreatorMedia(models.Model):
    name = models.CharField(max_length=255)
    media_files = GenericRelation('MediaFile') 

    def __str__(self):
        return self.name
 


class WriterMedia(models.Model):
    name = models.CharField(max_length=255)
    media_files = GenericRelation('MediaFile') 

    def __str__(self):
        return self.name

 
class MovieMedia(models.Model):
    name = models.CharField(max_length=255)
    media_files = GenericRelation('MediaFile')
    movie_slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs): 
        if not self.movie_slug :
            self.movie_slug= slugify(self.name)
        super().save(*args, **kwargs) 
    

    def __str__(self):
        return self.name 
    

class TVShowMedia(models.Model):
    name = models.CharField(max_length=255)
    tvshow_slug = models.SlugField(unique=True, blank=True)
    media_files = GenericRelation('MediaFile') 

    def save(self, *args, **kwargs):
        if not self.tvshow_slug:
            self.tvshow_slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class SeasonMedia(models.Model):
    tvshow = models.ForeignKey(TVShowMedia, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField()
    media_files = GenericRelation('MediaFile')

    class Meta:
        unique_together = ('tvshow', 'season_number')
        ordering = ['season_number']

    def __str__(self):
        return f"{self.tvshow.name} - Season {self.season_number}"


class EpisodeMedia(models.Model):
    tvshow = models.ForeignKey(TVShowMedia, on_delete=models.CASCADE, related_name='fk_seasons')
    season = models.ForeignKey(SeasonMedia, on_delete=models.CASCADE, related_name='episodes')  
    title = models.CharField(max_length=255)
    episode_number = models.PositiveIntegerField(editable=False)  # Auto-generated
    episode_slug = models.SlugField(unique=True, blank=True)
    media_files = GenericRelation('MediaFile') 

    class Meta:
        unique_together = ('tvshow','season','episode_number')    

    def save(self, *args, **kwargs):
        # Only for new episodes (not updates) when episode_number isn't set
        if not self.pk and not self.episode_number:
            # Get the highest episode number in this TV show + season
            last_episode = EpisodeMedia.objects.filter(
                tvshow=self.tvshow,
                season=self.season
            ).order_by('-episode_number').first()

            # Set the next episode number (last + 1, or 1 if no episodes exist)
            self.episode_number = (last_episode.episode_number + 1) if last_episode else 1

        # Auto-fill slug if empty
        if not self.episode_slug:
            self.episode_slug = slugify(self.title)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.season.tvshow.name} - S{self.season.season_number}E{self.episode_number}: {self.title}"



class MediaFile(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('banner', 'Banner'),
        ('thumbnail', 'Thumbnail'),
        ('trailer', 'Trailer'),
        ('video', 'Video'),
        ('profile_pic', 'Profile Picture'),
        ('related_pic', 'Related Picture'),
        ('other', 'Other'),     
    ]

    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='uploads/imdb_media/',  null=True, blank=True, storage=MediaCloudinaryStorage())
    cdn_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': [
                'moviemedia', 'tvshowmedia', 'seasonmedia', 'episodemedia',
                'castmedia', 'creatormedia', 'writermedia'
            ]
        }
    )

    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"ID-{self.object_id}: {self.media_type} for {self.related_object} ({self.content_type})"

