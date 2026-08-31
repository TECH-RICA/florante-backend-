"""Brevo transactional email — supports both API-key and SMTP-key modes.

Mode order:
  1. API key (BREVO_API_KEY, starts with xkeysib-)  -> REST API v3.
  2. SMTP key (EMAIL_HOST_USER + EMAIL_HOST_PASSWORD, password starts with
     xsmtpsib-)  -> SMTP relay via Django's send_mail.
"""

import json
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import send_mail

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def email_configured() -> bool:
    if getattr(settings, "BREVO_API_KEY", ""):
        return True
    return bool(getattr(settings, "EMAIL_HOST_USER", "") and getattr(settings, "EMAIL_HOST_PASSWORD", ""))


def _api_send(to: str, subject: str, body: str, html: str | None = None) -> tuple[bool, str]:
    payload = {
        "sender": {
            "name": getattr(settings, "DEFAULT_FROM_NAME", "") or "Florante Company Ltd",
            "email": getattr(settings, "DEFAULT_FROM_EMAIL", "") or "techrica2@gmail.com",
        },
        "to": [{"email": to}],
        "subject": subject,
    }
    if html:
        payload["htmlContent"] = html
    else:
        payload["textContent"] = body

    req = urllib.request.Request(
        BREVO_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": settings.BREVO_API_KEY,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status in (200, 201, 202):
                return True, "Email accepted by Brevo (API)."
            return False, f"Brevo returned status {resp.status}."
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return False, f"Brevo error {exc.code}: {detail}"
    except urllib.error.URLError as exc:
        return False, f"Could not reach Brevo: {exc.reason}"
    except TimeoutError:
        return False, "Timed out contacting Brevo."


def _smtp_send(to: str, subject: str, body: str, html: str | None = None) -> tuple[bool, str]:
    try:
        sent = send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL or "techrica2@gmail.com",
            [to],
            fail_silently=False,
            html_message=html,
        )
    except Exception as exc:  # noqa: BLE001
        return False, f"SMTP error: {exc}"
    if sent:
        return True, "Email sent via Brevo SMTP relay."
    return False, "SMTP send returned 0 — no email sent."


def send_brevo_email(to: str, subject: str, body: str, html: str | None = None) -> tuple[bool, str]:
    """Send a transactional email through Brevo. Returns (ok, detail)."""
    if getattr(settings, "BREVO_API_KEY", ""):
        ok, detail = _api_send(to, subject, body, html)
        if ok:
            return ok, detail
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            return _smtp_send(to, subject, body, html)
        return ok, detail
    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        return _smtp_send(to, subject, body, html)
    return False, "No Brevo key configured. Set BREVO_API_KEY or EMAIL_HOST_USER/EMAIL_HOST_PASSWORD in backend/.env."