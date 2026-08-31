from django.contrib import admin
from .models import Industry, Testimonial, University, TeamMember, FAQ


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "featured", "published")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author", "company", "role", "published", "created_at")
    list_filter = ("published",)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "county")
    search_fields = ("name",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "published")
    list_editable = ("order", "published")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "context", "order", "published")
    list_editable = ("order", "published")
    list_filter = ("context", "published")