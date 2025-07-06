import json, os
from django.core.management.base import BaseCommand
from app3_cast.models import Cast

class Command(BaseCommand):
    help = "Export JSON template with cast name and ID for CastCoreDetail"

    def handle(self, *args, **kwargs):
        output = []

        for cast in Cast.objects.all():
            # Skip if already has a core detail
            if hasattr(cast, 'core_detail'):
                continue

            output.append({
                "cast": {
                    "castmedia": cast.cast_name
                },
                "cast_id": cast.id,
                "height": "",
                "born_date": "",
                "death_date": "",
                "spouses": [],
                "children": [],
                "relatives": [],
                "otherwork": []
            })

        if not output:
            print("ℹ️ No Casts without CastCoreDetail found.")
            return

        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data/castcoredetail_template.json'
        )

        with open(file_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✅ Exported {len(output)} entries → {file_path}")
