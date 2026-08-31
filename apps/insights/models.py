from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify
from apps.cms.models import Industry


class Article(models.Model):
    """Insights / blog posts (Florante Intelligence)."""

    class Category(models.TextChoices):
        AI = "ai", "AI"
        CYBERSECURITY = "cybersecurity", "Cybersecurity"
        AFRICAN_TECH = "african-technology", "African Technology"
        SOFTWARE_ENGINEERING = "software-engineering", "Software Engineering"
        DIGITAL_TRANSFORMATION = "digital-transformation", "Digital Transformation"
        BUSINESS_TECH = "business-technology", "Business Technology"
        EDUCATION_TECH = "education-technology", "Education Technology"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    author_name = models.CharField(max_length=150, blank=True)
    author_role = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=40, choices=Category.choices, default=Category.AFRICAN_TECH)
    tags = ArrayField(models.CharField(max_length=80), default=list, blank=True)
    featured_image = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CaseStudy(models.Model):
    """Real projects that become sales assets (spec §27)."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    client = models.CharField(max_length=200)
    industry = models.ForeignKey(
        Industry, on_delete=models.SET_NULL, null=True, blank=True, related_name="case_studies"
    )
    challenge = models.TextField(blank=True)
    existing_situation = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    technologies = ArrayField(models.CharField(max_length=120), default=list, blank=True)
    implementation = models.TextField(blank=True)
    result = models.TextField(blank=True)
    client_quote = models.TextField(blank=True)
    client_quote_author = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="case-studies/", blank=True, null=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title