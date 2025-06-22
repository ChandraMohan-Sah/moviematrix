from django.db import models
from app1_media_manger.models import CreatorMedia
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from app1_media_manger.models import MovieMedia, TVShowMedia  # assuming these exist


class Creator(models.Model):
    """Main movie model in app6 with media integration"""
    creatormedia = models.OneToOneField(
        CreatorMedia,
        on_delete=models.CASCADE,
        related_name='app4_creator'
    )

    # Media access shortcut
    @property
    def creator_name(self):
        return self.creatormedia.name
    
    @property 
    def profile_pic(self):
        return self.creatormedia.media_files.filter(media_type='profile_pic')

    @property 
    def related_pic(self):
        return self.creatormedia.media_files.filter(media_type='related_pic')
    
    creator_created = models.DateTimeField(auto_now_add=True)
    creator_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator_name}"
    



class CreatorCoreDetail(models.Model):
    creator = models.OneToOneField(Creator, on_delete=models.CASCADE, related_name='creator_core_detail')
    height = models.CharField(max_length=20)
    born_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)
    
    spouses = models.ManyToManyField(Creator, related_name='spouse_of', blank=True)
    children = models.ManyToManyField(Creator, related_name='child_of', blank=True)
    relatives = models.ManyToManyField(Creator, related_name='relative_of', blank=True)

    otherwork = models.TextField(blank=True)

    def __str__(self):
        return f"Core Detail of {self.creator.creator_name}"




class CreatorKnownFor(models.Model):
    creator = models.ForeignKey(Creator,  on_delete=models.CASCADE, related_name='creator_known_for')

    content_type = models.ForeignKey(
        ContentType , 
        on_delete = models.CASCADE ,
        limit_choices_to = {
             'model__in': ['moviemedia', 'tvshowmedia']
        }
    )

    object_id = models.PositiveIntegerField() 
    known_work = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.creator.creator_name} known for {self.known_work}"
