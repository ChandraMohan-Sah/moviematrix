import json
import os
from django.core.management.base import BaseCommand
from app2_gener_platform.models import Genre

'''
Data Format:
[
  { "name": "Action" },
  { "name": "Comedy" }
]
'''

class Command(BaseCommand):
    help = "Bulk insert Genre"

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data/genre_data.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

        for item in data:
            name = item.get('name', '').strip()
            if not name:
                print("⚠️ Skipped empty genre name")
                continue

            if Genre.objects.filter(name__iexact=name).exists():
                print(f"⚠️ Skipped existing Genre Name: {name}")
                continue  # ✅ This prevents re-insertion

            genre = Genre.objects.create(name=name)
            print(f"✅ Created Genre: {genre.name}")
