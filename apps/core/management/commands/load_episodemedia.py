import json, os
from django.core.management.base import BaseCommand
from app1_media_manger.models import TVShowMedia, SeasonMedia, EpisodeMedia, MediaFile
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Bulk insert EpisodeMedia and MediaFiles without duplication"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'data/episodemedia_data.json')
        with open(file_path) as f:
            data = json.load(f)

        ct = ContentType.objects.get_for_model(EpisodeMedia)
        media_objs = []

        for item in data:
            tvshow_slug = item['tvshow']
            season_num = item['season_number']
            title = item['title'].strip()

            if not title:
                print("⚠️ Skipped episode with empty title")
                continue

            try:
                tvshow = TVShowMedia.objects.get(tvshow_slug=tvshow_slug)
                season = SeasonMedia.objects.get(tvshow=tvshow, season_number=season_num)
            except (TVShowMedia.DoesNotExist, SeasonMedia.DoesNotExist):
                print(f"❌ TVShow '{tvshow_slug}' or Season {season_num} missing. Skipping '{title}'")
                continue

            if EpisodeMedia.objects.filter(season=season, title=title).exists():
                print(f"⚠️ Episode '{title}' exists. Skipping.")
                continue

            episode = EpisodeMedia.objects.create(season=season, tvshow=tvshow, title=title, episode_slug=item.get('episode_slug', None))
            print(f"✅ Inserted Episode '{title}'")

            for mtype, urls in [('thumbnail', item.get('thumbnails', [])), ('video', item.get('videos', []))]:
                for url in urls:
                    media_objs.append(MediaFile(media_type=mtype, cdn_url=url, content_type=ct, object_id=episode.id))

        if media_objs:
            MediaFile.objects.bulk_create(media_objs)
            print(f"🎉 Inserted {len(media_objs)} MediaFiles")
