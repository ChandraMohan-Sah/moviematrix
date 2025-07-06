import json
import os
from django.core.management.base import BaseCommand
from app1_media_manger.models import WriterMedia, MediaFile
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Bulk insert WriterMedia and MediaFiles without duplication"

    def handle(self, *args, **kwargs):
        # Get JSON file path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data/writermedia_data.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

        writer_content_type = ContentType.objects.get_for_model(WriterMedia)
        media_objs = []

        for item in data:
            # Skip if WriterMedia already exists
            if WriterMedia.objects.filter(name=item['name']).exists():
                print(f"⚠️ Skipped existing WriterMedia: {item['name']}")
                continue

            # Create WriterMedia
            writer = WriterMedia.objects.create(name=item['name'])

            # Merge both profile and related pics with their types
            media_data = [
                ('profile_pic', item.get('profile_pics', [])),
                ('related_pic', item.get('related_pics', []))
            ]

            for media_type, urls in media_data:
                for url in urls:
                    media_objs.append(MediaFile(
                        media_type=media_type,
                        cdn_url=url,
                        content_type=writer_content_type,
                        object_id=writer.id
                    ))

            print(f"✅ Created WriterMedia: {writer.name}")

        # Bulk insert media
        if media_objs:
            MediaFile.objects.bulk_create(media_objs)
            print(f"🎉 Inserted {len(media_objs)} MediaFiles successfully.")
        else:
            print("ℹ️ No new media to insert.")



