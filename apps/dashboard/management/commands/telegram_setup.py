import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.dashboard import telegram as tg


class Command(BaseCommand):
    help = "Verify the Telegram bot, set the webhook, or poll for inbound messages (dev)."

    def add_arguments(self, parser):
        parser.add_argument("--check", action="store_true", help="Verify the bot token via getMe.")
        parser.add_argument("--poll", action="store_true", help="Long-poll for inbound messages (no webhook needed).")
        parser.add_argument("--url", default="", help="Webhook base URL (defaults to SITE_DOMAIN).")

    def handle(self, *args, **options):
        if not tg.bot_ready():
            raise CommandError("TELEGRAM_BOT_TOKEN is not set. Add it to backend/.env, then create a bot via @BotFather.")

        me, err = tg.get_me()
        if err:
            raise CommandError(f"Bot check failed: {err}")
        self.stdout.write(self.style.SUCCESS(f"Bot ok: @{me.get('username')} ({me.get('first_name')})"))

        if options["check"]:
            return

        if options["poll"]:
            self.stdout.write("Polling Telegram for messages (Ctrl+C to stop)...")
            offset = 0
            while True:
                updates, err = tg.get_updates()
                if err:
                    self.stdout.write(self.style.ERROR(err))
                    time.sleep(3)
                    continue
                for upd in updates:
                    offset = max(offset, upd.get("update_id", 0) + 1)
                    lead = tg.handle_update(upd)
                    if lead:
                        self.stdout.write(
                            f"  {lead.name} (@{lead.telegram_username}): {lead.message[:80]}"
                        )
                time.sleep(2)
            return

        domain = options["url"] or getattr(settings, "SITE_DOMAIN", "localhost:8000")
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        url = f"{domain}/api/telegram/webhook/"
        ok, detail = tg.set_webhook(url, settings.TELEGRAM_WEBHOOK_SECRET or None)
        if not ok:
            raise CommandError(detail)
        self.stdout.write(self.style.SUCCESS(f"Webhook set -> {url}"))
        self.stdout.write("  Note: Telegram cannot reach localhost. Use --poll for local testing.")