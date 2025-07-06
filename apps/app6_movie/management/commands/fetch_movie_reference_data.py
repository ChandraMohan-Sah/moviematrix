import json, os
from django.core.management.base import BaseCommand
from app2_gener_platform.models import Genre, Platform
from app3_cast.models import Cast
from app4_creator.models import Creator
from app5_writer.models import Writer

class Command(BaseCommand):
    help = "Generate JSON file listing all IDs and names for genres, platforms, casts, creators, writers"

    def handle(self, *args, **kwargs):
        data = {
            "genres": [{"id": g.id, "name": g.name} for g in Genre.objects.all()],
            "platforms": [{"id": p.id, "platform": p.platform} for p in Platform.objects.all()],
            "casts": [{"id": c.id, "cast_name": c.cast_name} for c in Cast.objects.select_related("castmedia")],
            "creators": [{"id": c.id, "creator_name": c.creator_name} for c in Creator.objects.select_related("creatormedia")],
            "writers": [{"id": w.id, "writer_name": w.writer_name} for w in Writer.objects.select_related("writermedia")]
        }

        output_path = os.path.join(os.path.dirname(__file__), "data/movie_reference_data.json")
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        self.stdout.write(self.style.SUCCESS("🎉 Reference data saved to movie_reference_data.json"))


