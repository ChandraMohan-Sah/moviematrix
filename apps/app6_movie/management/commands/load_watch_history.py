import json, os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app6_movie.models import Movie, MovieWatchHistory

User = get_user_model()

class Command(BaseCommand):
    help = "Load MovieWatchHistory from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "data/watch_history_data.json")
        with open(path) as f:
            data = json.load(f)

        for item in data:
            user = User.objects.filter(id=item["user_id"]).first()
            movie = Movie.objects.filter(id=item["movie_id"]).first()

            if not user or not movie:
                continue

            entry = MovieWatchHistory.objects.create(
                user=user,
                movie=movie,
                duration_watched=item.get("duration_watched"),
                is_completed=item.get("is_completed", False)
            )
            self.stdout.write(f"✅ Watch history added: {user.username} → {movie.title}")
