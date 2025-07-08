from django.contrib import admin
from .models import CacheEntry
# Register your models here.

@admin.register(CacheEntry)
class CacheEntryAdmin(admin.ModelAdmin):
    list_display = ('cache_key', 'expires')
    search_fields = ('cache_key',)
