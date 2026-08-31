from django.contrib import admin
from .models import Solution


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "published", "updated_at")
    list_filter = ("category", "published")
    search_fields = ("title", "slug", "short_description")
    prepopulated_fields = {"slug": ("title",)}