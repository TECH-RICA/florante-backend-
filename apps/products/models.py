from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify
from apps.cms.models import Industry, Testimonial


class Product(models.Model):
    """Products are managed from structured data, not hard-coded UI (spec §14)."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        BETA = "beta", "Beta"
        AVAILABLE = "available", "Available"
        COMING_SOON = "coming_soon", "Coming Soon"
        DEPRECATED = "deprecated", "Deprecated"

    class PricingType(models.TextChoices):
        ONE_TIME = "one_time", "One-time"
        MONTHLY = "monthly", "Monthly"
        ANNUAL = "annual", "Annual"
        CUSTOM = "custom", "Custom Quote"
        FREE = "free", "Free"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=100)
    short_description = models.TextField()
    long_description = models.TextField(blank=True)
    industries = models.ManyToManyField(Industry, related_name="products", blank=True)
    features = ArrayField(models.CharField(max_length=500), default=list, blank=True)
    benefits = ArrayField(models.CharField(max_length=500), default=list, blank=True)
    images = ArrayField(models.URLField(), default=list, blank=True)
    screenshots = ArrayField(models.URLField(), default=list, blank=True)
    pricing = models.CharField(max_length=120, blank=True, help_text="e.g. 'From KES 15,000'")
    pricing_type = models.CharField(max_length=20, choices=PricingType.choices, default=PricingType.CUSTOM)
    demo_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    technologies = ArrayField(models.CharField(max_length=120), default=list, blank=True)
    integrations = ArrayField(models.CharField(max_length=120), default=list, blank=True)
    faqs = models.JSONField(default=list, blank=True, help_text='List of {"question": "...", "answer": "..."}')
    testimonials = models.ManyToManyField(Testimonial, related_name="products", blank=True)
    target_customer = models.CharField(max_length=200, blank=True)
    problem_solved = models.TextField(blank=True)
    how_it_works = models.TextField(blank=True)
    security_notes = models.TextField(blank=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name