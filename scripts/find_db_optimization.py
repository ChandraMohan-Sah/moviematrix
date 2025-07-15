from django.apps import apps
from django.db.models.fields.related import (
    ForeignKey, OneToOneField, ManyToManyField, ManyToOneRel, ManyToManyRel
)

model = apps.get_model('app6_movie', 'MovieCoreDetail')

for field in model._meta.get_fields():
    if isinstance(field, (ForeignKey, OneToOneField)):
        print(f"{field.name}: select_related")
    elif isinstance(field, (ManyToManyField, ManyToManyRel, ManyToOneRel)):
        print(f"{field.name}: prefetch_related")

