from django.contrib import admin
from .models import Writer, WriterCoreDetail, WriterKnownFor
# Register your models here.


admin.site.register(Writer)
admin.site.register(WriterCoreDetail)
admin.site.register(WriterKnownFor)