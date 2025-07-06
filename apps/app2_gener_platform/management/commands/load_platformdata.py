import json
import os
from django.core.management.base import BaseCommand
from app2_gener_platform.models import Platform

'''
Data Format:
[
  { "platform": "Action" },
  { "platform": "Comedy" }
]
'''

class Command(BaseCommand):
    help = "Bulk insert Platform"

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data/platform_data.json')

        with open(file_path) as f:
            data = json.load(f)

        for item in data:
            plat = item.get('platform', '').strip()
            if not plat:
                print("⚠️ Skipped empty platform name")
                continue
            if Platform.objects.filter(platform__iexact=plat).exists():
                print(f"⚠️ Skipped existing Platform Name: {plat}")
                continue

            platform = Platform.objects.create(platform=plat)
            print(f"✅ Created Platform: {platform.platform}")
