import json, os
from django.core.management.base import BaseCommand
from app3_cast.models import Cast, CastCoreDetail

class Command(BaseCommand):
    help = "Bulk insert CastCoreDetail"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'data/castcoredetail_data.json')
        with open(path) as f: data = json.load(f)

        created, skipped = 0, 0

        for item in data:
            cast_id = item["cast_id"]
            try:
                cast = Cast.objects.get(id=cast_id)
            except Cast.DoesNotExist:
                print(f"❌ Cast ID {cast_id} not found")
                continue

            if hasattr(cast, 'core_detail'):
                print(f"⚠️ Skipped existing: {cast.cast_name}")
                skipped += 1
                continue

            CastCoreDetail.objects.create(
                cast=cast,
                height=item["height"],
                born_date=item["born_date"] or None,
                death_date=item["death_date"] or None,
                spouses=item["spouses"],
                children=item["children"],
                relatives=item["relatives"],
                otherwork=item["otherwork"]
            )
            print(f"✅ Created: {cast.cast_name}")
            created += 1

        print(f"\n🎉 Done — Created: {created}, Skipped: {skipped}")
