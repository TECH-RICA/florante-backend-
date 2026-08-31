"""Telegram bot integration for the dashboard inbox.

Sending: POST https://api.telegram.org/bot<TOKEN>/sendMessage
Receiving: webhook or getUpdates, processed into Lead records (source=telegram).
"""

import json
import urllib.error
import urllib.request

from django.conf import settings

from apps.leads.models import Lead

API_BASE = "https://api.telegram.org/bot"


def bot_ready() -> bool:
    return bool(getattr(settings, "TELEGRAM_BOT_TOKEN", ""))


def _call(method: str, data: dict | None = None, timeout: int = 20):
    if not bot_ready():
        return None, "Telegram bot token is not configured."
    url = f"{API_BASE}{settings.TELEGRAM_BOT_TOKEN}/{method}"
    body = json.dumps(data or {}).encode("utf-8") if data else None
    req = urllib.request.Request(
        url,
        data=body,
        headers={"content-type": "application/json"} if body else {},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return payload, ""
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return None, f"Telegram error {exc.code}: {detail}"
    except urllib.error.URLError as exc:
        return None, f"Could not reach Telegram: {exc.reason}"
    except TimeoutError:
        return None, "Timed out contacting Telegram."


def get_me() -> tuple[dict | None, str]:
    payload, err = _call("getMe")
    if err:
        return None, err
    if not payload.get("ok"):
        return None, f"Telegram says: {payload.get('description', 'unauthorized token')}"
    return payload.get("result"), ""


def send_message(chat_id: str | int, text: str) -> tuple[bool, str]:
    if not text.strip():
        return False, "Message is empty."
    payload, err = _call("sendMessage", {"chat_id": chat_id, "text": text})
    if err:
        return False, err
    if not payload.get("ok"):
        return False, f"Telegram says: {payload.get('description', 'send failed')}"
    return True, "Message sent via Telegram."


def set_webhook(url: str, secret: str | None = None) -> tuple[bool, str]:
    data = {"url": url, "allowed_updates": ["message"]}
    if secret:
        data["secret_token"] = secret
    payload, err = _call("setWebhook", data)
    if err:
        return False, err
    if not payload.get("ok"):
        return False, f"Telegram says: {payload.get('description', 'setWebhook failed')}"
    return True, payload.get("description", "Webhook set.")


def get_updates() -> tuple[list | None, str]:
    payload, err = _call("getUpdates", {"timeout": 5, "allowed_updates": ["message"]})
    if err:
        return None, err
    if not payload.get("ok"):
        return None, f"Telegram says: {payload.get('description', 'getUpdates failed')}"
    return payload.get("result", []), ""


def handle_update(update: dict) -> Lead | None:
    """Upsert a Lead from a Telegram update. Returns the lead (or None)."""
    message = update.get("message") or update.get("edited_message")
    if not message:
        return None
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if not chat_id:
        return None
    sender = message.get("from") or {}
    if sender.get("is_bot"):
        return None

    text = message.get("text") or ""
    first = (sender.get("first_name") or "").strip()
    last = (sender.get("last_name") or "").strip()
    username = (sender.get("username") or "").strip()
    name = " ".join(n for n in [first, last] if n).strip() or username or str(chat_id)

    lead, created = Lead.objects.get_or_create(
        telegram_chat_id=str(chat_id),
        defaults={
            "name": name,
            "category": Lead.Category.INDIVIDUAL,
            "email": "",
            "source": Lead.Source.TELEGRAM,
            "telegram_username": username,
            "message": text,
            "is_read": False,
        },
    )
    if not created:
        lead.name = name or lead.name
        lead.telegram_username = username or lead.telegram_username
        lead.message = text
        lead.is_read = False
        lead.save(update_fields=["name", "telegram_username", "message", "is_read", "updated_at"])
    return lead