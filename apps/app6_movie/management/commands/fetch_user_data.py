import json, os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Fetch all usernames and their IDs and save as JSON"

    def handle(self, *args, **kwargs):
        data = [{"id": user.id, "username": user.username} for user in User.objects.only("id", "username")]

        output_path = os.path.join(os.path.dirname(__file__), "data/user_reference_data.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        self.stdout.write(self.style.SUCCESS("🎉 User reference data saved to user_reference_data.json"))
