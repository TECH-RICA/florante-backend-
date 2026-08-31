from django.db import models
from apps.products.models import Product


class Lead(models.Model):
    """Unified lead record feeding the sales pipeline (spec §20–§23)."""

    class Source(models.TextChoices):
        CONTACT_FORM = "contact_form", "Contact Form"
        DEMO_REQUEST = "demo_request", "Demo Request"
        QUOTE_REQUEST = "quote_request", "Quote Request"
        NEWSLETTER = "newsletter", "Newsletter"
        WHATSAPP = "whatsapp", "WhatsApp"
        TELEGRAM = "telegram", "Telegram"
        PHONE = "phone", "Phone"
        EMAIL = "email", "Email"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUALIFIED = "qualified", "Qualified"
        MEETING_SCHEDULED = "meeting_scheduled", "Meeting Scheduled"
        DEMO = "demo", "Demo"
        PROPOSAL = "proposal", "Proposal"
        NEGOTIATION = "negotiation", "Negotiation"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    class Need(models.TextChoices):
        AI = "ai", "AI"
        CYBERSECURITY = "cybersecurity", "Cybersecurity"
        WEBSITE = "website", "Website"
        MOBILE_APP = "mobile_app", "Mobile App"
        ENTERPRISE_SYSTEM = "enterprise_system", "Enterprise System"
        AUTOMATION = "automation", "Automation"
        DIGITAL_TRANSFORMATION = "digital_transformation", "Digital Transformation"
        PRODUCT = "product", "Product"
        OTHER = "other", "Other"

    class Category(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        ORGANIZATION = "organization", "Organization"

    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.ORGANIZATION
    )
    organization = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    industry = models.CharField(max_length=120, blank=True)
    need = models.CharField(max_length=40, choices=Need.choices, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    budget_range = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.CONTACT_FORM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    lead_score = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    telegram_chat_id = models.CharField(max_length=40, blank=True)
    telegram_username = models.CharField(max_length=120, blank=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_leads"
    )
    next_action = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.email})"