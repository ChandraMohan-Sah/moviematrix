import json, os
from django.core.management.base import BaseCommand
from app6_movie.models import Movie, MovieTechSpecs

class Command(BaseCommand):
    help = "Load MovieTechSpecs from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "data/movietechspecs_data.json")
        with open(path) as f:
            data = json.load(f)

        for item in data:
            movie = Movie.objects.filter(id=item["movie_id"]).first()
            if not movie:
                self.stdout.write(f"❌ Movie ID {item['movie_id']} not found")
                continue
            if hasattr(movie, 'movie_tech_specs'):
                self.stdout.write(f"⚠️ Skipping existing TechSpecs for {movie.title}")
                continue

            MovieTechSpecs.objects.create(
                movie=movie,
                runtime=item["runtime"],
                color=item["color"],
                sound_mix=item["sound_mix"]
            )
            self.stdout.write(f"✅ Created TechSpecs for {movie.title}")
