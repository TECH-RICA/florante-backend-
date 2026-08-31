from django.db import models
from django.utils.text import slugify


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Industry(TimestampedModel):
    """Industry verticals Florante serves (Education, SMEs, Financial Services, ...)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="industries/", blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Optional icon name")
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Industries"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Testimonial(TimestampedModel):
    quote = models.TextField()
    author = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author} — {self.company}"


class University(TimestampedModel):
    name = models.CharField(max_length=200, unique=True)
    county = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Universities"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TeamMember(TimestampedModel):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True, help_text="URL of the member's photo (upload from the admin panel).")
    portfolio_url = models.URLField(blank=True, help_text="Link to the member's portfolio.")
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class FAQ(TimestampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    context = models.CharField(max_length=100, blank=True, help_text="e.g. products, cybersecurity, general")
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question