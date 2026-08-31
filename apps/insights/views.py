from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Article, CaseStudy
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    CaseStudySerializer,
)


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleDetailSerializer
        return ArticleListSerializer

    def get_queryset(self):
        qs = Article.objects.filter(is_published=True)
        params = self.request.query_params

        category = params.get("category")
        featured = params.get("featured")
        search = params.get("search")

        if category:
            qs = qs.filter(category=category)
        if featured:
            qs = qs.filter(is_featured=True)
        if search:
            qs = qs.filter(
                Q(title__icontains=search)
                | Q(excerpt__icontains=search)
                | Q(content__icontains=search)
                | Q(tags__icontains=search)
            )
        return qs.order_by("-published_at", "-created_at")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=["views_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ArticleCategoriesAPIView(ListAPIView):
    def list(self, request):
        categories = [
            {"slug": c.value, "label": c.label}
            for c in Article.Category
        ]
        return Response(categories)


class CaseStudyViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = None
    serializer_class = CaseStudySerializer

    def get_queryset(self):
        qs = CaseStudy.objects.filter(published=True)
        industry = self.request.query_params.get("industry")
        if industry:
            qs = qs.filter(industry__slug=industry)
        return qs.order_by("-created_at")