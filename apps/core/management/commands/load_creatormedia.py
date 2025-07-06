import json
import os
from django.core.management.base import BaseCommand
from app1_media_manger.models import CreatorMedia, MediaFile
from django.contrib.contenttypes.models import ContentType


'''
    steps :
        - class defination
        - handle method : main function that rubs when executed command
        - locate and load JSON data 
        - prepare for linking MediaFile to CastMedia
        - process each CastMedia record from JSON
        - avoid duplicate CastMedia 
        - create new CastMedia 
        - prepare MediaFile data to associate with CastMedia 
        - create MediaFile objects (in memory)
        - log creations
        - bulk insert MediaFiles
        
'''



class Command(BaseCommand):
    help = "Bulk insert CreatorMedia and MediaFiles without duplication"

    def handle(self, *args, **kwargs):
        # Get JSON file path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data/creatormedia_data.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

        creator_content_type = ContentType.objects.get_for_model(CreatorMedia)
        media_objs = []

        for item in data:
            # Skip if CreatorMedia already exists
            if CreatorMedia.objects.filter(name=item['name']).exists():
                print(f"⚠️ Skipped existing CreatorMedia: {item['name']}")
                continue

            # Create CreatorMedia
            creator = CreatorMedia.objects.create(name=item['name'])

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
                        content_type=creator_content_type,
                        object_id=creator.id
                    ))

            print(f"✅ Created CreatorMedia: {creator.name}")

        # Bulk insert media
        if media_objs:
            MediaFile.objects.bulk_create(media_objs)
            print(f"🎉 Inserted {len(media_objs)} MediaFiles successfully.")
        else:
            print("ℹ️ No new media to insert.")



