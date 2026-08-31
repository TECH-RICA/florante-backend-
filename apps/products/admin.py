from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "pricing", "status", "published", "updated_at")
    list_filter = ("status", "pricing_type", "published", "category")
    search_fields = ("name", "slug", "category", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("industries", "testimonials")