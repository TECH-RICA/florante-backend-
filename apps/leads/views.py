from rest_framework import generics
from rest_framework.throttling import ScopedRateThrottle
from .models import Lead
from .serializers import LeadCreateSerializer


class LeadThrottle(ScopedRateThrottle):
    scope = "lead"


class LeadCreateView(generics.CreateAPIView):
    """Universal lead capture — Talk to Florante / contact form."""
    serializer_class = LeadCreateSerializer
    throttle_classes = [LeadThrottle]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["source"] = self.request.data.get("source", Lead.Source.CONTACT_FORM)
        return context


class DemoRequestView(generics.CreateAPIView):
    serializer_class = LeadCreateSerializer
    throttle_classes = [LeadThrottle]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["source"] = Lead.Source.DEMO_REQUEST
        return context


class QuoteRequestView(generics.CreateAPIView):
    serializer_class = LeadCreateSerializer
    throttle_classes = [LeadThrottle]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["source"] = Lead.Source.QUOTE_REQUEST
        return context


class NewsletterSignupView(generics.CreateAPIView):
    """Newsletter signup — minimal name/email lead."""

    class NewsletterSerializer(LeadCreateSerializer):
        class Meta(LeadCreateSerializer.Meta):
            fields = ["name", "email"]

    serializer_class = NewsletterSerializer
    throttle_classes = [LeadThrottle]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["source"] = Lead.Source.NEWSLETTER
        return context