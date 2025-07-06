from django.core.management.base import BaseCommand
from app1_media_manger.models import CreatorMedia
from app4_creator.models import Creator  # adjust if your app name is different

class Command(BaseCommand):
    help = "Create Creator for all existing CreatorMedia without duplicates"

    def handle(self, *args, **kwargs):
        created, skipped = 0, 0

        for cm in CreatorMedia.objects.all():
            if Creator.objects.filter(creatormedia=cm).exists():
                skipped += 1
                continue
            Creator.objects.create(creatormedia=cm)
            created += 1
            print(f"✅ Created Creator for: {cm.name}")

        print(f"\n🎉 Done! Created: {created}, Skipped: {skipped}")
