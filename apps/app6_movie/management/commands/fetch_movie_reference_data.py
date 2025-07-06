import json, os
from django.core.management.base import BaseCommand

from app2_gener_platform.models import Genre, Platform
from app3_cast.models import Cast
from app4_creator.models import Creator
from app5_writer.models import Writer
from app8_lang_prod_company.models import Language, ProductionCompany  

class Command(BaseCommand):
    help = "Generate JSON file listing all IDs and names for genres, platforms, casts, creators, writers, languages, and production companies"

    def handle(self, *args, **kwargs):
        data = {
            "genres": [{"id": g.id, "name": g.name} for g in Genre.objects.all()],
            "platforms": [{"id": p.id, "platform": p.platform} for p in Platform.objects.all()],
            "casts": [{"id": c.id, "cast_name": c.cast_name} for c in Cast.objects.select_related("castmedia")],
            "creators": [{"id": c.id, "creator_name": c.creator_name} for c in Creator.objects.select_related("creatormedia")],
            "writers": [{"id": w.id, "writer_name": w.writer_name} for w in Writer.objects.select_related("writermedia")],
            "languages": [{"id": l.id, "language": l.language} for l in Language.objects.all()],
            "production_companies": [{"id": pc.id, "production_company": pc.production_company} for pc in ProductionCompany.objects.all()]
        }

        output_path = os.path.join(os.path.dirname(__file__), "data/movie_reference_data.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        self.stdout.write(self.style.SUCCESS("🎉 Reference data saved to movie_reference_data.json"))

