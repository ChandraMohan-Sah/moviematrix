import json, os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app6_movie.models import Movie, MovieVotes

User = get_user_model()

class Command(BaseCommand):
    help = "Load MovieVotes from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "data/votes_data.json")
        with open(path) as f:
            data = json.load(f)

        for item in data:
            user = User.objects.filter(id=item["user_id"]).first()
            movie = Movie.objects.filter(id=item["movie_id"]).first()
            vote_type = item["vote_type"]

            if not user or not movie:
                continue

            obj, created = MovieVotes.objects.get_or_create(
                user_vote=user, movie=movie, defaults={"vote_type": vote_type}
            )
            if not created:
                self.stdout.write(f"⚠️ Vote already exists for {user.username} → {movie.title}")
            else:
                self.stdout.write(f"✅ {user.username} voted '{vote_type}' for {movie.title}")
