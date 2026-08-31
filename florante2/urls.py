from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from apps.dashboard.views import (
    TrackVisitView,
    HeartbeatView,
    ActivityLogView,
    TelegramWebhookView,
)


def health(request):
    return JsonResponse({"status": "ok", "service": "Florante 2.0 API"})


urlpatterns = [
    path("sanctum-backend-admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/", include("apps.core.urls")),
    path("api/admin/", include("apps.dashboard.urls")),
    path("api/analytics/track/", TrackVisitView.as_view(), name="analytics-track"),
    path("api/analytics/heartbeat/", HeartbeatView.as_view(), name="analytics-heartbeat"),
    path("api/analytics/activity/", ActivityLogView.as_view(), name="analytics-activity"),
    path("api/telegram/webhook/", TelegramWebhookView.as_view(), name="telegram-webhook"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)