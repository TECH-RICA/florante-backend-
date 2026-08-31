from rest_framework import serializers
from .models import Product
from apps.cms.serializers import TestimonialSerializer


class ProductListSerializer(serializers.ModelSerializer):
    industries = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category", "short_description",
            "pricing", "pricing_type", "status", "target_customer", "industries",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    industries = serializers.StringRelatedField(many=True, read_only=True)
    testimonials = TestimonialSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category", "short_description", "long_description",
            "industries", "features", "benefits", "images", "screenshots",
            "pricing", "pricing_type", "demo_url", "status",
            "technologies", "integrations", "faqs", "testimonials",
            "target_customer", "problem_solved", "how_it_works", "security_notes",
            "seo_title", "seo_description", "created_at", "updated_at",
        ]