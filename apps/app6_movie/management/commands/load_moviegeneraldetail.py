import os, json
from django.core.management.base import BaseCommand
from app6_movie.models import Movie, MovieGeneralDetail

class Command(BaseCommand):
    help = "Bulk insert MovieGeneralDetail from JSON file"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'data/moviegeneraldetail_data.json')
        with open(path) as f:
            data = json.load(f)

        created, skipped = 0, 0

        for item in data:
            movie_id = item["movie_id"]
            try:
                movie = Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                self.stdout.write(f"❌ Movie ID {movie_id} not found.")
                continue

            if hasattr(movie, 'movie_general_detail'):
                self.stdout.write(f"⚠️ Skipped existing: {movie.title}")
                skipped += 1
                continue

            MovieGeneralDetail.objects.create(
                movie=movie,
                active=item["active"],
                is_original=item["is_original"],
                duration=item["duration"],
                avg_rating=item["avg_rating"],
                number_rating=item["number_rating"],
                storyline=item["storyline"]
            )
            self.stdout.write(f"✅ Created Movie General Detail for : {movie.title}")
            created += 1

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done — Created: {created}, Skipped: {skipped}"))
