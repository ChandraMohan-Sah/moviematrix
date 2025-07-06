import json, os
from django.core.management.base import BaseCommand
from app5_writer.models import Writer, WriterCoreDetail

class Command(BaseCommand):
    help = "Export JSON template with writer name and ID for WriterCoreDetail"

    def handle(self, *args, **kwargs):
        output = []

        for wr in Writer.objects.all():
            # Skip if already has a core detail
            if hasattr(wr, 'core_detail'):
                continue

            output.append({
                "writer": {
                    "writermedia": wr.writer_name
                },
                "writer_id": wr.id,
                "height": "",
                "born_date": "",
                "death_date": "",
                "spouses": [],
                "children": [],
                "relatives": [],
                "otherwork": []
            })

        if not output:
            print("ℹ️ No Writers without WriterCoreDetail found.")
            return

        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data/writercoredetail_template.json'
        )

        with open(file_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✅ Exported {len(output)} entries → {file_path}")



