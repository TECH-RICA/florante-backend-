import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Run all migrations, seeds, and create initial admin user automatically"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=== Running Migrations ==="))
        call_command("migrate", interactive=False)

        self.stdout.write(self.style.NOTICE("=== Seeding Production Data ==="))
        call_command("seed_industries")
        call_command("seed_solutions")
        call_command("seed_products")
        call_command("seed_articles")
        call_command("seed_cms")
        call_command("seed_case_studies")
        call_command("seed_hackathons")

        # Admin user creation
        email = os.environ.get("ADMIN_EMAIL", "admin@florante.tech").strip()
        password = os.environ.get("ADMIN_PASSWORD", "FloranteAdmin2026!").strip()
        username = email.split("@")[0]

        if not User.objects.filter(email__iexact=email).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name="Florante",
                last_name="Admin",
            )
            self.stdout.write(self.style.SUCCESS(f"=== Superuser '{email}' created successfully ==="))
        else:
            self.stdout.write(self.style.NOTICE(f"=== Superuser '{email}' already exists ==="))

        self.stdout.write(self.style.SUCCESS("=== Production Database Setup Complete ==="))
