import json, os
from django.core.management.base import BaseCommand
from app5_writer.models import Writer, WriterCoreDetail

class Command(BaseCommand):
    help = "Bulk insert WriterCoreDetail"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'data/writercoredetail_data.json')
        with open(path) as f: data = json.load(f)

        created, skipped = 0, 0

        for item in data:
            writer_id = item["writer_id"]
            try:
                writer = Writer.objects.get(id=writer_id)
            except Writer.DoesNotExist:
                print(f"❌ Writer ID {writer_id} not found")
                continue

            if hasattr(writer, 'writer_core_detail'):
                print(f"⚠️ Skipped existing: {writer.writer_name}")
                skipped += 1
                continue

            WriterCoreDetail.objects.create(
                writer=writer,
                height=item["height"],
                born_date=item["born_date"] or None,
                death_date=item["death_date"] or None,
                spouses=item["spouses"],
                children=item["children"],
                relatives=item["relatives"],
                otherwork=item["otherwork"]
            )
            print(f"✅ Created: {writer.writer_name}")
            created += 1

        print(f"\n🎉 Done — Created: {created}, Skipped: {skipped}")
