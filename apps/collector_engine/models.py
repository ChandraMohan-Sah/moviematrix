from django.db import models
from django.contrib import admin

# Dynamically define a model pointing to your cached table
class CacheEntry(models.Model):
    cache_key = models.CharField(max_length=255, primary_key=True)
    value = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        db_table = 'cached_table'  # <-- Use the same LOCATION name
        verbose_name = 'Cache Entry'
        verbose_name_plural = 'Cache Entries'

    def __str__(self):
        return self.cache_key


