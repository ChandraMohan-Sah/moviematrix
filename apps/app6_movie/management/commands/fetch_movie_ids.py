import json, os
from django.core.management.base import BaseCommand
from app6_movie.models import Movie

class Command(BaseCommand):
    help = "Export all movie IDs with titles into a JSON file"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.select_related('moviemedia').only('id', 'moviemedia__name')
        data = [{"id": movie.id, "title": movie.title} for movie in movies]

        output_path = os.path.join(os.path.dirname(__file__), 'data/movie_ids.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        self.stdout.write(self.style.SUCCESS("🎬 Movie IDs exported to movie_ids.json"))
