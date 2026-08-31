from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify


class Solution(models.Model):
    """Core solution areas — sell outcomes, not activities (spec §16)."""

    class Category(models.TextChoices):
        AI_AUTOMATION = "ai-automation", "AI & Automation"
        CYBERSECURITY = "cybersecurity", "Cybersecurity"
        SOFTWARE_ENGINEERING = "software-engineering", "Software Engineering"
        DIGITAL_TRANSFORMATION = "digital-transformation", "Digital Transformation"
        DATA_INTELLIGENCE = "data-intelligence", "Data & Intelligence"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=40, choices=Category.choices)
    short_description = models.TextField()
    hero_text = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    approach = models.TextField(blank=True)
    capabilities = ArrayField(models.CharField(max_length=500), default=list, blank=True)
    use_cases = ArrayField(models.CharField(max_length=500), default=list, blank=True)
    benefits = ArrayField(models.CharField(max_length=500), default=list, blank=True)
    technologies = ArrayField(models.CharField(max_length=120), default=list, blank=True)
    faqs = models.JSONField(default=list, blank=True, help_text='List of {"question": "...", "answer": "..."}')
    image = models.ImageField(upload_to="solutions/", blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True)
    cta_text = models.CharField(max_length=120, blank=True, default="Talk to Florante")
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title