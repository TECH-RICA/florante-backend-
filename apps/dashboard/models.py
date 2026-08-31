from django.db import models
from django.utils import timezone


class AnalyticsVisit(models.Model):
    class Device(models.TextChoices):
        MOBILE = "mobile", "Mobile"
        TABLET = "tablet", "Tablet"
        DESKTOP = "desktop", "Desktop"

    path = models.CharField(max_length=500, default="/")
    referrer = models.CharField(max_length=500, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True, default="")
    device = models.CharField(max_length=20, choices=Device.choices, default=Device.DESKTOP)
    session_key = models.CharField(max_length=64, blank=True, default="")
    is_authenticated = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-viewed_at"]
        indexes = [models.Index(fields=["viewed_at"]), models.Index(fields=["path"])]

    def __str__(self):
        return f"{self.path} @ {self.viewed_at:%Y-%m-%d %H:%M}"


class PageSession(models.Model):
    """Accumulated time spent on a page per browser session."""

    session_key = models.CharField(max_length=64, blank=True, default="")
    path = models.CharField(max_length=500, default="/")
    device = models.CharField(max_length=20, default="desktop")
    referrer = models.CharField(max_length=500, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    entered_at = models.DateTimeField(default=timezone.now)
    last_active_at = models.DateTimeField(default=timezone.now)
    duration_seconds = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-last_active_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["session_key", "path"], name="uniq_page_session"
            )
        ]
        indexes = [
            models.Index(fields=["last_active_at"]),
            models.Index(fields=["path"]),
        ]

    def __str__(self):
        return f"{self.path} · {self.duration_seconds}s"


class SectionEngagement(models.Model):
    """Accumulated time and views per section on a page per session."""

    session_key = models.CharField(max_length=64, blank=True, default="")
    path = models.CharField(max_length=500, default="/")
    section = models.CharField(max_length=120, default="")
    duration_seconds = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=1)
    first_seen_at = models.DateTimeField(default=timezone.now)
    last_active_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-last_active_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["session_key", "path", "section"], name="uniq_section_engagement"
            )
        ]
        indexes = [models.Index(fields=["path", "section"])]

    def __str__(self):
        return f"{self.path}#{self.section} · {self.duration_seconds}s"


class ActivityLog(models.Model):
    """Individual user actions (CTA clicks, searches, scroll depth, etc.)."""

    session_key = models.CharField(max_length=64, blank=True, default="")
    path = models.CharField(max_length=500, blank=True, default="")
    action = models.CharField(max_length=60, db_index=True)
    label = models.CharField(max_length=255, blank=True, default="")
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"]), models.Index(fields=["action"])]

    def __str__(self):
        return f"{self.action} · {self.label} @ {self.created_at:%H:%M}"


class AdminAudit(models.Model):
    """Readable trail of what staff did in the admin — who, what, when."""

    class Action(models.TextChoices):
        CREATED = "created", "Created"
        UPDATED = "updated", "Updated"
        DELETED = "deleted", "Deleted"
        REPLIED = "replied", "Replied"
        ARCHIVED = "archived", "Archived"
        UNARCHIVED = "unarchived", "Unarchived"
        MARKED_READ = "marked_read", "Marked read"
        MARKED_UNREAD = "marked_unread", "Marked unread"
        UPLOADED = "uploaded", "Uploaded"
        SENT_TEST = "sent_test", "Sent test email"
        SENT_TELEGRAM = "sent_telegram", "Sent Telegram message"

    actor = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="admin_audits"
    )
    action = models.CharField(max_length=30, choices=Action.choices, default=Action.CREATED)
    resource = models.CharField(max_length=60, blank=True, default="")
    resource_id = models.PositiveIntegerField(null=True, blank=True)
    summary = models.CharField(max_length=400, blank=True, default="")
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["action"]),
            models.Index(fields=["resource"]),
        ]

    def __str__(self):
        return f"{self.action} · {self.summary} @ {self.created_at:%Y-%m-%d %H:%M}"
