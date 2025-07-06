import json, os
from django.core.management.base import BaseCommand
from app6_movie.models import Movie, MovieCoreDetail, Language, ProductionCompany

class Command(BaseCommand):
    help = "Load MovieCoreDetail from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "data/moviecoredetail_data.json")
        with open(path) as f:
            data = json.load(f)

        for item in data:
            movie = Movie.objects.filter(id=item["movie_id"]).first()
            if not movie:
                self.stdout.write(f"❌ Movie ID {item['movie_id']} not found")
                continue
            if hasattr(movie, 'movie_core_detail'):
                self.stdout.write(f"⚠️ Skipping existing MovieCoreDetail for {movie.title}")
                continue

            detail = MovieCoreDetail.objects.create(
                movie=movie,
                release_date=item["release_date"],
                country_of_origin=item["country_of_origin"],
                also_known_as=item["also_known_as"],
                filming_location=item["filming_location"]
            )
            detail.language.set(Language.objects.filter(id__in=item["language_ids"]))
            detail.production_companies.set(ProductionCompany.objects.filter(id__in=item["production_company_ids"]))
            self.stdout.write(f"✅ Created MovieCoreDetail for {movie.title}")
