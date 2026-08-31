import html
import re
from rest_framework import serializers
from .models import Lead


def _sanitize_string(val):
    if not isinstance(val, str):
        return val
    cleaned = re.sub(r'<script.*?>.*?</script>', '', val, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<iframe.*?>.*?</iframe>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'on\w+=".*?"', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
    return html.escape(cleaned.strip(), quote=True)


class LeadSerializer(serializers.ModelSerializer):
    """Public serializer — read/write for website lead capture."""

    class Meta:
        model = Lead
        fields = [
            "id", "name", "category", "organization", "email", "phone", "industry",
            "need", "product", "budget_range", "message", "source",
            "created_at",
        ]
        read_only_fields = ["id", "source", "created_at"]


class LeadCreateSerializer(serializers.ModelSerializer):
    """Write-only serializer used by the website forms with security sanitization."""

    class Meta:
        model = Lead
        fields = [
            "name", "category", "organization", "email", "phone", "industry",
            "need", "product", "budget_range", "message",
        ]

    def validate(self, attrs):
        for field in ["name", "organization", "phone", "industry", "message"]:
            if field in attrs and attrs[field]:
                attrs[field] = _sanitize_string(attrs[field])
        if "email" in attrs and attrs["email"]:
            attrs["email"] = attrs["email"].strip().lower()
        return attrs

    def create(self, validated_data):
        source = self.context.get("source", Lead.Source.CONTACT_FORM)
        lead = Lead.objects.create(source=source, **validated_data)
        lead.lead_score = self._score(lead)
        lead.save(update_fields=["lead_score"])
        return lead

    @staticmethod
    def _score(lead):
        score = 0
        if lead.email and "@" in lead.email:
            domain = lead.email.split("@")[1].lower()
            if domain not in ("gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"):
                score += 10
        if lead.need == Lead.Need.ENTERPRISE_SYSTEM:
            score += 20
        if lead.need == Lead.Need.AI:
            score += 15
        if lead.product:
            score += 20
        return score