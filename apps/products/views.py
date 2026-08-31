from django.db.models import Q
from rest_framework import viewsets
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.filter(published=True)
        params = self.request.query_params

        category = params.get("category")
        industry = params.get("industry")
        status = params.get("status")
        pricing_type = params.get("pricing_type")
        search = params.get("search")

        if category:
            qs = qs.filter(category__iexact=category)
        if industry:
            qs = qs.filter(industries__slug=industry)
        if status:
            qs = qs.filter(status=status)
        if pricing_type:
            qs = qs.filter(pricing_type=pricing_type)
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(short_description__icontains=search)
                | Q(category__icontains=search)
                | Q(problem_solved__icontains=search)
                | Q(target_customer__icontains=search)
            )
        return qs.order_by("-created_at")