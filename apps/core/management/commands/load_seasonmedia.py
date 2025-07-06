import json
import os
from django.core.management.base import BaseCommand
from app1_media_manger.models import SeasonMedia, MediaFile, TVShowMedia
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Bulk insert SeasonMedia and associated MediaFiles without duplication"

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(BASE_DIR, 'data/seasonmedia_data.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

        season_content_type = ContentType.objects.get_for_model(SeasonMedia)
        media_objs = []

        for item in data:
            tvshow_slug = item['tvshow']
            season_number = item['season_number']

            try:
                tvshow_obj = TVShowMedia.objects.get(tvshow_slug=tvshow_slug)
            except TVShowMedia.DoesNotExist:
                print(f"❌ TVShow with slug '{tvshow_slug}' not found. Skipping.")
                continue

            # Check for duplicate season per TV show
            if SeasonMedia.objects.filter(tvshow=tvshow_obj, season_number=season_number).exists():
                print(f"⚠️ Skipped existing Season {season_number} for TVShow '{tvshow_slug}'")
                continue

            # Create SeasonMedia (no name field)
            season = SeasonMedia.objects.create(
                tvshow=tvshow_obj,
                season_number=season_number
            )

            media_data = [
                ('banners', item.get('banners', [])),
                ('thumbnail', item.get('thumbnails', []))
            ]

            for media_type, urls in media_data:
                for url in urls:
                    media_objs.append(MediaFile(
                        media_type=media_type,
                        cdn_url=url,
                        content_type=season_content_type,
                        object_id=season.id
                    ))

            print(f"✅ Created Season {season_number} for TVShow '{tvshow_slug}'")

        if media_objs:
            MediaFile.objects.bulk_create(media_objs)
            print(f"🎉 Inserted {len(media_objs)} MediaFiles successfully.")
        else:
            print("ℹ️ No new media to insert.")
