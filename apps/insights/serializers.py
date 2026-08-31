from rest_framework import serializers
from .models import Article, CaseStudy


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "excerpt", "category", "featured_image",
            "author_name", "author_role", "published_at", "views_count", "tags",
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "excerpt", "content", "category", "tags",
            "featured_image", "author_name", "author_role", "is_featured",
            "views_count", "published_at",
            "seo_title", "seo_description",
        ]


class CaseStudySerializer(serializers.ModelSerializer):
    industry = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CaseStudy
        fields = [
            "id", "title", "slug", "client", "industry", "challenge",
            "existing_situation", "solution", "technologies", "implementation",
            "result", "client_quote", "client_quote_author", "image",
            "seo_title", "seo_description", "created_at",
        ]