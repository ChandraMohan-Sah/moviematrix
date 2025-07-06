import os, json
from django.core.management.base import BaseCommand
from app8_lang_prod_company.models import ProductionCompany  # Replace with your app

class Command(BaseCommand):
    help = "Bulk insert production companies from JSON"

    def handle(self, *args, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'data/production_company_data.json')
        with open(path) as f:
            data = json.load(f)

        created, skipped = 0, 0

        for item in data:
            name = item.get("production_company", "").strip()
            if not name:
                self.stdout.write("⚠️ Skipped empty production company")
                continue
            if ProductionCompany.objects.filter(production_company__iexact=name).exists():
                self.stdout.write(f"⚠️ Skipped existing: {name}")
                skipped += 1
                continue

            ProductionCompany.objects.create(production_company=name)
            self.stdout.write(f"✅ Created: {name}")
            created += 1

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done — Created: {created}, Skipped: {skipped}"))


