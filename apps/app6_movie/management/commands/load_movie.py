import json, os
from django.core.management.base import BaseCommand
from app6_movie.models import Movie, MovieMedia
from app2_gener_platform.models import Genre, Platform
from app3_cast.models import Cast
from app4_creator.models import Creator
from app5_writer.models import Writer

class Command(BaseCommand):
    help = "Bulk insert Movie using existing media and relationships"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(os.path.dirname(__file__), 'data/movie_data.json')

        with open(json_path) as f:
            movie_data = json.load(f)

        created, skipped = 0, 0

        for item in movie_data:
            try:
                mm = MovieMedia.objects.get(movie_slug=item["moviemedia"])
            except MovieMedia.DoesNotExist:
                print(f"❌ MovieMedia '{item['moviemedia']}' not found.")
                continue

            if hasattr(mm, 'app6_movie'):
                print(f"⚠️ Movie already exists: {mm.name}")
                skipped += 1
                continue

            try:
                platform = Platform.objects.get(id=item["platform_id"])
            except Platform.DoesNotExist:
                print(f"❌ Platform ID {item['platform_id']} not found.")
                continue

            movie = Movie.objects.create(moviemedia=mm, platform=platform)

            movie.movie_genre.set(Genre.objects.filter(id__in=item["movie_genre_ids"]))
            movie.movie_cast.set(Cast.objects.filter(id__in=item["movie_cast_ids"]))
            movie.movie_creator.set(Creator.objects.filter(id__in=item["movie_creator_ids"]))
            movie.movie_writer.set(Writer.objects.filter(id__in=item["movie_writer_ids"]))

            print(f"✅ Movie created: {movie.title}")
            created += 1

        print(f"\n🎬 Done — Created: {created}, Skipped: {skipped}")
