import json, os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app6_movie.models import Movie, UserMovieWatchlist

User = get_user_model()

class Command(BaseCommand):
    help = "Load UserMovieWatchlist from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "data/watchlist_data.json")
        with open(path) as f:
            data = json.load(f)

        for item in data:
            user = User.objects.filter(id=item["user_id"]).first()
            movie = Movie.objects.filter(id=item["movie_id"]).first()

            if not user or not movie:
                continue

            obj, created = UserMovieWatchlist.objects.get_or_create(user_watchlist=user, movie=movie)
            msg = "✅ Created" if created else "⚠️ Already exists"
            self.stdout.write(f"{msg}: {user.username} → {movie.title}")
