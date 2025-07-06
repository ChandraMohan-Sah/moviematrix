import json
import os
from django.core.management.base import BaseCommand
from app1_media_manger.models import TVShowMedia, MediaFile
from django.contrib.contenttypes.models import ContentType

'''
Data Format :
{
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
  ],
  "name": "string",  [required]
  "tvshow_slug": "string"
}
'''

class Command(BaseCommand):
    help = "Bulk insert TVShowMedia and MediaFiles without duplication"

    def handle(self, *args, **kwargs):
        # Get JSON file path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data/tvshowmedia_data.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

        tvshow_content_type = ContentType.objects.get_for_model(TVShowMedia)
        media_objs = []

        for item in data:
            # Skip if TVshowMedia already exists
            if TVShowMedia.objects.filter(name=item['name']).exists():
                print(f"⚠️ Skipped existing TVShowMedia: {item['name']}")
                continue

            # Create TVShowMedia
            tvshow = TVShowMedia.objects.create(name=item['name'])

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
                        content_type=tvshow_content_type,
                        object_id=tvshow.id
                    ))

            print(f"✅ Created TVShow: {tvshow.name}")

        # Bulk insert media
        if media_objs:
            MediaFile.objects.bulk_create(media_objs)
            print(f"🎉 Inserted {len(media_objs)} MediaFiles successfully.")
        else:
            print("ℹ️ No new media to insert.")



