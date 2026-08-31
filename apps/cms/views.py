from rest_framework import viewsets
from .models import Industry, Testimonial, University, TeamMember, FAQ
from .serializers import (
    IndustrySerializer,
    TestimonialSerializer,
    UniversitySerializer,
    TeamMemberSerializer,
    FAQSerializer,
)


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IndustrySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Industry.objects.filter(published=True).order_by("name")


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TestimonialSerializer
    pagination_class = None

    def get_queryset(self):
        return Testimonial.objects.filter(published=True)


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UniversitySerializer
    pagination_class = None

    def get_queryset(self):
        qs = University.objects.order_by("name")
        q = self.request.query_params.get("search")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamMemberSerializer
    pagination_class = None

    def get_queryset(self):
        return TeamMember.objects.filter(published=True).order_by("order", "name")


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FAQSerializer
    pagination_class = None

    def get_queryset(self):
        qs = FAQ.objects.filter(published=True).order_by("order")
        context = self.request.query_params.get("context")
        if context:
            qs = qs.filter(context=context)
        return qs