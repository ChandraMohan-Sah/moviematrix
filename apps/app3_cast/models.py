from django.db import models
from app1_media_manger.models import CastMedia
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from app1_media_manger.models import MovieMedia, TVShowMedia  # assuming these exist


class Cast(models.Model):
    """Main movie model in app6 with media integration"""
    castmedia = models.OneToOneField(
        CastMedia,
        on_delete=models.CASCADE,
        related_name='app3_cast',
        help_text="write name of CastMedia"
    )

    # Media access shortcut
    @property
    def cast_name(self):
        return self.castmedia.name
    
    @property 
    def profile_pic(self):
        return self.castmedia.media_files.filter(media_type='profile_pic')

    @property 
    def related_pic(self):
        return self.castmedia.media_files.filter(media_type='related_pic')
    
    cast_created = models.DateTimeField(auto_now_add=True)
    cast_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cast_name}"
    


class CastCoreDetail(models.Model):
    cast = models.OneToOneField(Cast, on_delete=models.CASCADE, related_name='core_detail')
    height = models.CharField(max_length=20)
    born_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)
    
    spouses = models.JSONField(default=list, blank=True)
    children = models.JSONField(default=list, blank=True)
    relatives = models.JSONField(default=list, blank=True)  
    otherwork = models.JSONField(default=list, blank=True) 

    def __str__(self):
        return f"Core Detail of {self.cast.cast_name}"




# class CastKnownFor(models.Model):
#     cast = models.ForeignKey(Cast,  on_delete=models.CASCADE, related_name='known_for')

#     content_type = models.ForeignKey(
#         ContentType , 
#         on_delete = models.CASCADE ,
#         limit_choices_to = {
#              'model__in': ['moviemedia', 'tvshowmedia']
#         }
#     )

#     object_id = models.PositiveIntegerField() 
#     known_work = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return f"{self.cast.cast_name} known for {self.known_work}"
