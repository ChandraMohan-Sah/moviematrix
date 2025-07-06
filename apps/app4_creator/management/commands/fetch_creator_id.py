import json, os
from django.core.management.base import BaseCommand
from app4_creator.models import Creator

class Command(BaseCommand):
    help = "Export JSON template with cast name and ID for CastCoreDetail"

    def handle(self, *args, **kwargs):
        output = []

        for create in Creator.objects.all():
            # Skip if already has a core detail
            if hasattr(create, 'core_detail'):
                continue

            output.append({
                "creator": {
                    "creatormedia": create.creator_name
                },
                "creator_id": create.id,
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
            'data/creatorcoredetail_template.json'
        )

        with open(file_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✅ Exported {len(output)} entries → {file_path}")
