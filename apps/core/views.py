from rest_framework import viewsets, mixins
from rest_framework.generics import RetrieveAPIView
from .models import SiteConfig
from .serializers import SiteConfigSerializer


class SiteConfigViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """Public site configuration (contact info, socials)."""
    queryset = SiteConfig.objects.all()
    serializer_class = SiteConfigSerializer
    lookup_field = "pk"

    def get_object(self):
        return SiteConfig.load()