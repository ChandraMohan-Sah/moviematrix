from django.core.management.base import BaseCommand
from app1_media_manger.models import CastMedia
from app3_cast.models import Cast  # adjust if your app name is different

class Command(BaseCommand):
    help = "Create Cast for all existing CastMedia without duplicates"

    def handle(self, *args, **kwargs):
        created, skipped = 0, 0

        for cm in CastMedia.objects.all():
            if Cast.objects.filter(castmedia=cm).exists():
                skipped += 1
                continue
            Cast.objects.create(castmedia=cm)
            created += 1
            print(f"✅ Created Cast for: {cm.name}")

        print(f"\n🎉 Done! Created: {created}, Skipped: {skipped}")
