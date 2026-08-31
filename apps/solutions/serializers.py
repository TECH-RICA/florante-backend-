from rest_framework import serializers
from .models import Solution


class SolutionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "title", "slug", "category", "short_description", "icon", "cta_text"]


class SolutionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = [
            "id", "title", "slug", "category", "short_description", "hero_text",
            "problem", "approach", "capabilities", "use_cases", "benefits",
            "technologies", "faqs", "image", "icon", "cta_text",
            "seo_title", "seo_description",
        ]