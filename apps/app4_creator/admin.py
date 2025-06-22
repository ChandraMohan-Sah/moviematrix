from django.contrib import admin
from .models import Creator, CreatorCoreDetail, CreatorKnownFor

# Register your models here.
admin.site.register(Creator)
admin.site.register(CreatorCoreDetail)
admin.site.register(CreatorKnownFor)

