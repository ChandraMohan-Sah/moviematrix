from django.contrib import admin
from .models import Cast, CastCoreDetail, CastKnownFor

# Register your models here.
admin.site.register(Cast)
admin.site.register(CastCoreDetail)
admin.site.register(CastKnownFor)
