from django.core.management.base import BaseCommand
from app1_media_manger.models import WriterMedia
from app5_writer.models import Writer  # adjust if your app name is different

class Command(BaseCommand):
    help = "Create Writer for all existing WriterMedia without duplicates"

    def handle(self, *args, **kwargs):
        created, skipped = 0, 0

        for wm in WriterMedia.objects.all():
            if Writer.objects.filter(writermedia=wm).exists():
                skipped += 1
                continue
            Writer.objects.create(writermedia=wm)
            created += 1
            print(f"✅ Created Writer for: {wm.name}")

        print(f"\n🎉 Done! Created: {created}, Skipped: {skipped}")


