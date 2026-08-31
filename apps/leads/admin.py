from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "email", "phone", "need", "source", "status", "lead_score", "created_at")
    list_filter = ("status", "source", "need", "industry")
    search_fields = ("name", "organization", "email", "phone", "message")
    list_editable = ("status", "lead_score")
    date_hierarchy = "created_at"