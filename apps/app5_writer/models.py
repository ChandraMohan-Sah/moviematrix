from django.db import models
from app1_media_manger.models import WriterMedia
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from app1_media_manger.models import MovieMedia, TVShowMedia  # assuming these exist


class Writer(models.Model):
    """Main movie model in app6 with media integration"""
    writermedia = models.OneToOneField(
        WriterMedia,
        on_delete=models.CASCADE,
        related_name='app5_writer'
    )

    # Media access shortcut
    @property
    def writer_name(self):
        return self.writermedia.name
    
    @property 
    def profile_pic(self):
        return self.writermedia.media_files.filter(media_type='profile_pic')

    @property 
    def related_pic(self):
        return self.writermedia.media_files.filter(media_type='related_pic')
    
    writer_created = models.DateTimeField(auto_now_add=True)
    writer_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.writer_name}"
    



class WriterCoreDetail(models.Model):
    writer = models.OneToOneField(Writer, on_delete=models.CASCADE, related_name='writer_core_detail')
    height = models.CharField(max_length=20)
    born_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)
    
    spouses = models.ManyToManyField(Writer, related_name='spouse_of', blank=True)
    children = models.ManyToManyField(Writer, related_name='child_of', blank=True)
    relatives = models.ManyToManyField(Writer, related_name='relative_of', blank=True)

    otherwork = models.TextField(blank=True)

    def __str__(self):
        return f"Core Detail of {self.writer.writer_name}"




class WriterKnownFor(models.Model):
    writer = models.ForeignKey(Writer,  on_delete=models.CASCADE, related_name='writer_known_for')

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
        return f"{self.writer.writer_name} known for {self.known_work}"


