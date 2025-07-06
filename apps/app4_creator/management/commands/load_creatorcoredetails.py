import json, os
from django.core.management.base import BaseCommand
from app4_creator.models import Creator, CreatorCoreDetail

class Command(BaseCommand):
    help = "Bulk insert CreatorCoreDetail"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'data/creatorcoredetail_data.json')
        with open(path) as f: data = json.load(f)

        created, skipped = 0, 0

        for item in data:
            creator_id = item["creator_id"]
            try:
                creator = Creator.objects.get(id=creator_id)
            except Creator.DoesNotExist:
                print(f"❌ Creator ID {creator_id} not found")
                continue

            if hasattr(creator, 'core_detail'):
                print(f"⚠️ Skipped existing: {creator.creator_name}")
                skipped += 1
                continue

            CreatorCoreDetail.objects.create(
                creator=creator,
                height=item["height"],
                born_date=item["born_date"] or None,
                death_date=item["death_date"] or None,
                spouses=item["spouses"],
                children=item["children"],
                relatives=item["relatives"],
                otherwork=item["otherwork"]
            )
            print(f"✅ Created: {creator.creator_name}")
            created += 1

        print(f"\n🎉 Done — Created: {created}, Skipped: {skipped}")
