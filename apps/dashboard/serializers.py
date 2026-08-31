from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.cms.models import Industry, Testimonial, University, TeamMember, FAQ
from apps.products.models import Product
from apps.solutions.models import Solution
from apps.insights.models import Article, CaseStudy
from apps.leads.models import Lead
from apps.labs.models import Hackathon
from apps.core.models import SiteConfig
from .models import AnalyticsVisit, AdminAudit

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "is_superuser"]


class ProductAdminSerializer(serializers.ModelSerializer):
    industries = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Industry.objects.all(), required=False
    )
    testimonials = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Testimonial.objects.all(), required=False
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class SolutionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "image"]


class ArticleAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "views_count"]


class CaseStudyAdminSerializer(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(
        queryset=Industry.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = CaseStudy
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "image"]


class IndustryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "image"]


class TestimonialAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "image"]


class UniversityAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class TeamMemberAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class FAQAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class LeadAdminSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=False, allow_null=True
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Lead
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class HackathonAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class SiteConfigAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = "__all__"
        read_only_fields = ["id", "updated_at"]


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsVisit
        fields = "__all__"
        read_only_fields = [
            "id",
            "ip_address",
            "user_agent",
            "device",
            "session_key",
            "is_authenticated",
            "viewed_at",
        ]


class AdminAuditSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    actor_email = serializers.SerializerMethodField()

    class Meta:
        model = AdminAudit
        fields = [
            "id", "actor", "actor_name", "actor_email", "action",
            "resource", "resource_id", "summary", "meta", "created_at",
        ]
        read_only_fields = fields

    def get_actor_name(self, obj):
        if not obj.actor:
            return "System"
        name = f"{obj.actor.first_name} {obj.actor.last_name}".strip()
        return name or obj.actor.username

    def get_actor_email(self, obj):
        return obj.actor.email if obj.actor else ""
