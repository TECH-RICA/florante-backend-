import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Run all migrations, seeds, and ensure admin superuser credentials"

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

        # Admin user creation / password sync
        email = os.environ.get("ADMIN_EMAIL", "admin@florante.tech").strip().lower()
        password = os.environ.get("ADMIN_PASSWORD", "FloranteAdmin2026!").strip()
        username = os.environ.get("ADMIN_USERNAME", email.split("@")[0]).strip()

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            user = User.objects.filter(username__iexact=username).first()

        if not user:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name="Florante",
                last_name="Admin",
            )
            self.stdout.write(self.style.SUCCESS(f"=== Created superuser '{email}' ==="))
        else:
            user.email = email
            user.username = username
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"=== Updated superuser '{email}' password & staff privileges ==="))

        self.stdout.write(self.style.SUCCESS("=== Production Database Setup Complete ==="))
