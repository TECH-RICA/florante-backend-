from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views import SiteConfigViewSet
from apps.cms.views import (
    IndustryViewSet,
    TestimonialViewSet,
    UniversityViewSet,
    TeamMemberViewSet,
    FAQViewSet,
)
from apps.products.views import ProductViewSet
from apps.solutions.views import SolutionViewSet
from apps.insights.views import ArticleViewSet, ArticleCategoriesAPIView, CaseStudyViewSet
from apps.leads.views import (
    LeadCreateView,
    DemoRequestView,
    QuoteRequestView,
    NewsletterSignupView,
)
from apps.labs.views import HackathonViewSet

router = DefaultRouter()
router.register(r"site", SiteConfigViewSet, basename="site")
router.register(r"industries", IndustryViewSet, basename="industry")
router.register(r"testimonials", TestimonialViewSet, basename="testimonial")
router.register(r"universities", UniversityViewSet, basename="university")
router.register(r"team", TeamMemberViewSet, basename="team")
router.register(r"faqs", FAQViewSet, basename="faq")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"solutions", SolutionViewSet, basename="solution")
router.register(r"insights", ArticleViewSet, basename="article")
router.register(r"case-studies", CaseStudyViewSet, basename="case-study")
router.register(r"hackathons", HackathonViewSet, basename="hackathon")

urlpatterns = [
    path("leads/", LeadCreateView.as_view(), name="lead-create"),
    path("leads/demo-request/", DemoRequestView.as_view(), name="demo-request"),
    path("leads/quote-request/", QuoteRequestView.as_view(), name="quote-request"),
    path("leads/newsletter/", NewsletterSignupView.as_view(), name="newsletter"),
    path("site/", SiteConfigViewSet.as_view({"get": "retrieve"}), name="site"),
    path("insights/categories/", ArticleCategoriesAPIView.as_view(), name="article-categories"),
    path("", include(router.urls)),
]