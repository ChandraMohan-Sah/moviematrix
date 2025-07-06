import json
import os
from django.core.management.base import BaseCommand
from app1_media_manger.models import MovieMedia, MediaFile
from django.contrib.contenttypes.models import ContentType

'''
Data Format :
{
  "name": "string",
  "banners": [
    "http://example.com"
  ],
  "thumbnails": [
    "http://example.com"
  ],
  "trailers": [
    "http://example.com"
  ],
  "videos": [
    "http://example.com"
  ],
  "related_pics": [
    "http://example.com"
  ]
}

'''

class Command(BaseCommand):
    help = "Bulk insert MovieMedia and MediaFiles without duplication"

    def handle(self, *args, **kwargs):
        # Get JSON file path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data/moviemedia_data.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

        movie_content_type = ContentType.objects.get_for_model(MovieMedia)
        media_objs = []

        for item in data:
            # Skip if MovieMedia already exists
            if MovieMedia.objects.filter(name=item['name']).exists():
                print(f"⚠️ Skipped existing MovieMedia: {item['name']}")
                continue

            # Create MovieMedia
            movie = MovieMedia.objects.create(name=item['name'])

            # Merge both profile and related pics with their types
            media_data = [
                ('banners', item.get('banners',[])),
                ('thumbnail', item.get('thumbnails', [])),
                ('trailer', item.get('trailers', [])),
                ('videos', item.get('videos', [])),
                ('related_pic', item.get('related_pics', []))
            ]

            for media_type, urls in media_data:
                for url in urls:
                    media_objs.append(MediaFile(
                        media_type=media_type,
                        cdn_url=url,
                        content_type=movie_content_type,
                        object_id=movie.id
                    ))

            print(f"✅ Created MovieMedia: {movie.name}")

        # Bulk insert media
        if media_objs:
            MediaFile.objects.bulk_create(media_objs)
            print(f"🎉 Inserted {len(media_objs)} MediaFiles successfully.")
        else:
            print("ℹ️ No new media to insert.")



