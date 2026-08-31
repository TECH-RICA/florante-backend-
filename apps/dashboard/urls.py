from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ADMIN_VIEWSETS,
    AdminAuditListView,
    AdminLoginView,
    AdminLogoutView,
    AdminMeView,
    AdminTelegramView,
    AdminTestEmailView,
    AdminUploadView,
    AdminUserListView,
    AdminUserDetailView,
    DashboardStatsView,
    SiteConfigAdminView,
    HeartbeatView,
    ActivityLogView,
)

router = DefaultRouter()
for name, viewset in ADMIN_VIEWSETS.items():
    router.register(name, viewset, basename=f"admin-{name}")

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("logout/", AdminLogoutView.as_view(), name="admin-logout"),
    path("me/", AdminMeView.as_view(), name="admin-me"),
    path("upload/", AdminUploadView.as_view(), name="admin-upload"),
    path("test-email/", AdminTestEmailView.as_view(), name="admin-test-email"),
    path("telegram/", AdminTelegramView.as_view(), name="admin-telegram"),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
    path("audit/", AdminAuditListView.as_view(), name="admin-audit"),
    path("dashboard/", DashboardStatsView.as_view(), name="admin-dashboard"),
    path("site/", SiteConfigAdminView.as_view(), name="admin-site"),
    path("", include(router.urls)),
]
