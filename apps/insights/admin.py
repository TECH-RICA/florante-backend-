from django.contrib import admin
from .models import Article, CaseStudy


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author_name", "is_featured", "is_published", "views_count", "published_at")
    list_filter = ("category", "is_featured", "is_published")
    search_fields = ("title", "slug", "excerpt")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "industry", "published", "created_at")
    list_filter = ("industry", "published")
    search_fields = ("title", "client", "challenge")
    prepopulated_fields = {"slug": ("title",)}