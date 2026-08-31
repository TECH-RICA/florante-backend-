from django.contrib import admin

from .models import ActivityLog, AdminAudit, AnalyticsVisit, PageSession, SectionEngagement


@admin.register(AdminAudit)
class AdminAuditAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "action", "resource", "summary")
    list_filter = ("action", "resource")
    search_fields = ("summary", "actor__username", "actor__email")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in AdminAudit._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AnalyticsVisit)
class AnalyticsVisitAdmin(admin.ModelAdmin):
    list_display = ("path", "device", "viewed_at")
    list_filter = ("device",)
    search_fields = ("path",)
    date_hierarchy = "viewed_at"
    readonly_fields = [f.name for f in AnalyticsVisit._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "label", "path")
    list_filter = ("action",)
    search_fields = ("label", "path")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in ActivityLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PageSession)
class PageSessionAdmin(admin.ModelAdmin):
    list_display = ("path", "duration_seconds", "last_active_at")
    date_hierarchy = "last_active_at"
    readonly_fields = [f.name for f in PageSession._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SectionEngagement)
class SectionEngagementAdmin(admin.ModelAdmin):
    list_display = ("path", "section", "views_count", "duration_seconds")
    readonly_fields = [f.name for f in SectionEngagement._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False