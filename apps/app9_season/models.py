# from django.db import models
# from app1_media_manger.models import SeasonMedia

# # Create your models here.
# class Season(models.Model):
#     seasonmedia = models.OneToOneField(
#         SeasonMedia,
#         on_delete=models.CASCADE,
#         related_name="app9_season"
#     )

#     @property 
#     def title(self):
#         return self.seasonmedia.tvshow.name
    
#     @property 
#     def season_number(self):
#         return self.seasonmedia.season_number 
    
#     season_created = models.DateTimeField(auto_now_add=True)
#     season_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"TVShow - {self.title} have Season - {self.season_number}"
    
    
 