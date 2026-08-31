from rest_framework import viewsets
from .models import Solution
from .serializers import SolutionListSerializer, SolutionDetailSerializer


class SolutionViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SolutionDetailSerializer
        return SolutionListSerializer

    def get_queryset(self):
        qs = Solution.objects.filter(published=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs.order_by("category", "title")