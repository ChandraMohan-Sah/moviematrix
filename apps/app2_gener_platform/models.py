from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Platform(models.Model):
    platform = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.platform 
    
 