from rest_framework import viewsets
from .models import Hackathon
from .serializers import HackathonSerializer


class HackathonViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = None
    serializer_class = HackathonSerializer

    def get_queryset(self):
        qs = Hackathon.objects.filter(published=True)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("start_date")