from django.contrib import admin
from .models import Hackathon


@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "start_date", "deadline", "participants_count", "published")
    list_filter = ("status", "published")
    search_fields = ("title", "tagline", "description")
    prepopulated_fields = {"slug": ("title",)}