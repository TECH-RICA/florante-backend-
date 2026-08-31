from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.dashboard.brevo import email_configured, send_brevo_email


class Command(BaseCommand):
    help = "Send a test email through the Brevo transactional API to verify setup."

    def add_arguments(self, parser):
        parser.add_argument("to", nargs="?", default="", help="Recipient email address.")
        parser.add_argument(
            "--check",
            action="store_true",
            help="Only report whether the Brevo API key is configured (no email sent).",
        )

    def handle(self, *args, **options):
        if options["check"]:
            if not email_configured():
                self.stderr.write(
                    self.style.ERROR("Brevo API key is not configured. Add BREVO_API_KEY to backend/.env")
                )
                raise CommandError("BREVO_API_KEY missing.")
            self.stdout.write(self.style.SUCCESS("Brevo API key is configured."))
            self.stdout.write(f"  api={getattr(settings, 'BREVO_API_KEY', '')[:12]}…")
            self.stdout.write(f"  from={settings.DEFAULT_FROM_EMAIL}")
            return

        to = (options["to"] or "").strip()
        if not to:
            raise CommandError("Provide a recipient address, e.g. manage.py send_test_email you@example.com")
        if not email_configured():
            raise CommandError("Brevo API key is not configured. Add BREVO_API_KEY to backend/.env.")

        subject = "Brevo test email — Florante"
        body = (
            "Hello,\n\n"
            "This is a test email sent through the Brevo transactional API configured "
            "for the Florante site. If you received this, email replies are fully working.\n\n"
            "— Florante Tech"
        )
        ok, detail = send_brevo_email(to, subject, body)
        if not ok:
            raise CommandError(f"Email failed: {detail}")
        self.stdout.write(self.style.SUCCESS(f"Test email sent to {to}. {detail}"))