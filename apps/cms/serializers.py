from rest_framework import serializers
from .models import Industry, Testimonial, University, TeamMember, FAQ


class IndustrySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Industry
        fields = ["id", "name", "slug", "short_description", "description", "image", "icon", "products_count"]

    def get_products_count(self, obj):
        return obj.products.filter(published=True).count()


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "quote", "author", "role", "company", "image"]


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "county"]


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "role",
            "bio",
            "image",
            "portfolio_url",
            "linkedin",
            "github",
            "twitter",
        ]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "context"]