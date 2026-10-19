
import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Reset an existing admin password using an environment variable"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError(
                "Set DJANGO_ADMIN_USERNAME and DJANGO_ADMIN_PASSWORD "
                "in the hosting environment first."
            )

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(
                f"Admin username '{username}' was not found."
            )

        user.set_password(password)
        user.save(update_fields=["password"])

        self.stdout.write(
            self.style.SUCCESS("Admin password reset successfully.")
        )
