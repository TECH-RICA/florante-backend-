from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify


class Hackathon(models.Model):
    """Florante Labs — hackathons, projects and experiments (spec IA)."""

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ONGOING = "ongoing", "Ongoing"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    tech_stack = ArrayField(models.CharField(max_length=120), default=list, blank=True)
    prizes = models.JSONField(default=list, blank=True)
    schedule = models.JSONField(default=list, blank=True)
    sponsors = ArrayField(models.CharField(max_length=120), default=list, blank=True)
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)
    participants_count = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title