import os, json
from django.core.management.base import BaseCommand
from app8_lang_prod_company.models import Language  # Replace with your actual app name

class Command(BaseCommand):
    help = "Bulk insert languages from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'data/language_data.json')
        with open(path) as f:
            data = json.load(f)

        created, skipped = 0, 0

        for item in data:
            name = item.get("language", "").strip()
            if not name:
                self.stdout.write("⚠️ Skipped empty language")
                continue
            if Language.objects.filter(language__iexact=name).exists():
                self.stdout.write(f"⚠️ Skipped existing: {name}")
                skipped += 1
                continue
            Language.objects.create(language=name)
            self.stdout.write(f"✅ Created: {name}")
            created += 1

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done — Created: {created}, Skipped: {skipped}"))


