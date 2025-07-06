import json, os
from django.core.management.base import BaseCommand
from app6_movie.models import Movie, MovieBoxOffice

class Command(BaseCommand):
    help = "Load MovieBoxOffice from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "data/movieboxoffice_data.json")
        with open(path) as f:
            data = json.load(f)

        for item in data:
            movie = Movie.objects.filter(id=item["movie_id"]).first()
            if not movie:
                self.stdout.write(f"❌ Movie ID {item['movie_id']} not found")
                continue
            if hasattr(movie, 'movie_box_office'):
                self.stdout.write(f"⚠️ Skipping existing BoxOffice for {movie.title}")
                continue

            MovieBoxOffice.objects.create(
                movie=movie,
                budget=item["budget"],
                gross_country=item["gross_country"],
                opening_weekend=item["opening_weekend"],
                gross_worldwide=item["gross_worldwide"]
            )
            self.stdout.write(f"✅ Created BoxOffice for {movie.title}")
