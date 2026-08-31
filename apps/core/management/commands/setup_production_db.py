import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Run all migrations, seeds, and ensure superuser credentials for user"

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

        # Admin user creation / password sync for user's email
        email = os.environ.get("ADMIN_EMAIL", "njugunawilson977@gmil.com").strip().lower()
        password = os.environ.get("ADMIN_PASSWORD", "27580072@Willy").strip()
        username = email.split("@")[0]

        emails_to_provision = [email, "njugunawilson977@gmail.com"]

        for target_email in emails_to_provision:
            target_username = target_email.split("@")[0]
            user = User.objects.filter(email__iexact=target_email).first()
            if not user:
                user = User.objects.filter(username__iexact=target_username).first()

            if not user:
                user = User.objects.create_superuser(
                    username=target_username,
                    email=target_email,
                    password=password,
                    first_name="Willy",
                    last_name="Maina",
                )
                self.stdout.write(self.style.SUCCESS(f"=== Created superuser '{target_email}' ==="))
            else:
                user.email = target_email
                user.username = target_username
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"=== Synced superuser '{target_email}' password & staff privileges ==="))

        self.stdout.write(self.style.SUCCESS("=== Production Database Setup Complete ==="))
