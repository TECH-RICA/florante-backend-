from rest_framework import serializers
from .models import SiteConfig


class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = [
            "site_name", "tagline", "description",
            "primary_email", "secondary_email", "phone", "whatsapp",
            "address", "city", "linkedin", "github", "twitter", "facebook",
        ]