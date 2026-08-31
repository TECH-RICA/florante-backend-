from datetime import timedelta

from django.utils import timezone
from celery import shared_task

from .models import AnalyticsVisit, PageSession, SectionEngagement, ActivityLog


@shared_task
def cleanup_analytics(days: int = 90) -> str:
    """Delete analytics rows older than `days` days to keep the DB lean."""
    cutoff = timezone.now() - timedelta(days=days)
    deleted = {}
    for name, model, field in (
        ("visits", AnalyticsVisit, "viewed_at"),
        ("page_sessions", PageSession, "last_active_at"),
        ("section_engagement", SectionEngagement, "last_active_at"),
        ("activity_logs", ActivityLog, "created_at"),
    ):
        deleted[name] = model.objects.filter(**{f"{field}__lt": cutoff}).delete()[0]
    return f"cleanup deleted: {deleted}"