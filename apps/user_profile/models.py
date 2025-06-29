from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True, storage=MediaCloudinaryStorage())

    @property 
    def username(self):
        return self.user.username 
    
    @property 
    def email(self):
        return self.user.email
    
    @property 
    def date_joined(self):
        return self.user.date_joined
    
    def __str__(self):
        return self.user.username
    
    