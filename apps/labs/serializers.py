from rest_framework import serializers
from .models import Hackathon


class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = [
            "id", "title", "slug", "tagline", "description", "long_description",
            "rules", "tech_stack", "prizes", "schedule", "sponsors",
            "start_date", "deadline", "status", "participants_count", "image",
        ]