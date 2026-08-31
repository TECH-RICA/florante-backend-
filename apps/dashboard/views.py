from datetime import timedelta
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.files.storage import default_storage
from django.db.models import Count, Max, Q, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.utils.crypto import get_random_string

from rest_framework import mixins, status, views, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from apps.core.models import SiteConfig
from apps.cms.models import Industry, Testimonial, University, TeamMember, FAQ
from apps.dashboard.brevo import email_configured, send_brevo_email
from apps.dashboard import telegram as tg
from apps.products.models import Product
from apps.solutions.models import Solution
from apps.insights.models import Article, CaseStudy
from apps.leads.models import Lead
from apps.labs.models import Hackathon

from .models import AnalyticsVisit, PageSession, SectionEngagement, ActivityLog, AdminAudit
from .serializers import (
    AdminUserSerializer,
    AdminAuditSerializer,
    SiteConfigAdminSerializer,
    ProductAdminSerializer,
    SolutionAdminSerializer,
    ArticleAdminSerializer,
    CaseStudyAdminSerializer,
    IndustryAdminSerializer,
    TestimonialAdminSerializer,
    UniversityAdminSerializer,
    TeamMemberAdminSerializer,
    FAQAdminSerializer,
    LeadAdminSerializer,
    HackathonAdminSerializer,
    VisitSerializer,
)

User = get_user_model()


def _audit(user, action, resource, obj=None, resource_id=None, summary="", meta=None):
    """Create an AdminAudit row for a staff action."""
    if obj is not None and resource_id is None:
        resource_id = getattr(obj, "id", None)
    AdminAudit.objects.create(
        actor=user if user and user.is_authenticated else None,
        action=action,
        resource=resource,
        resource_id=resource_id,
        summary=summary or str(obj or ""),
        meta=meta or {},
    )


class AdminCRUDViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Generic staff-only CRUD endpoint with search support."""
    permission_classes = [IsAdminUser]
    pagination_class = None
    search_fields = []
    resource_key = ""

    def get_queryset(self):
        qs = self.queryset
        search = self.request.query_params.get("search")
        if search and self.search_fields:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f"{field}__icontains": search})
            qs = qs.filter(q)
        return qs

    def perform_create(self, serializer):
        obj = serializer.save()
        _audit(
            self.request.user,
            AdminAudit.Action.CREATED,
            self.resource_key,
            obj,
            summary=f"Created {self.resource_key}: {obj}",
        )

    def perform_update(self, serializer):
        obj = serializer.save()
        _audit(
            self.request.user,
            AdminAudit.Action.UPDATED,
            self.resource_key,
            obj,
            summary=f"Updated {self.resource_key}: {obj}",
        )

    def perform_destroy(self, instance):
        resource = self.resource_key
        summary = str(instance)
        resource_id = instance.id
        super().perform_destroy(instance)
        _audit(
            self.request.user,
            AdminAudit.Action.DELETED,
            resource,
            resource_id=resource_id,
            summary=f"Deleted {resource}: {summary}",
        )


# ---- Auth ------------------------------------------------------------------


class AdminLoginThrottle(ScopedRateThrottle):
    scope = "admin_login"


class AdminLoginView(views.APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AdminLoginThrottle]

    def post(self, request):
        identifier = (request.data.get("email") or request.data.get("username") or "").strip()
        password = request.data.get("password", "")
        if not identifier or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(Q(email__iexact=identifier) | Q(username__iexact=identifier)).first()
        if user is None:
            user = authenticate(request, username=identifier, password=password)
        else:
            if not user.check_password(password):
                user = None

        if user is None or not user.is_staff or not user.is_active:
            return Response(
                {"detail": "Invalid credentials or account is not an active staff member."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": AdminUserSerializer(user).data,
            }
        )


class AdminLogoutView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        if getattr(request, "auth", None):
            request.auth.delete()
        return Response({"detail": "Logged out."})


class AdminMeView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(AdminUserSerializer(request.user).data)


class AdminUploadView(views.APIView):
    """Accept an uploaded file and return a public URL to store on a record."""

    permission_classes = [IsAdminUser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "No file was provided."}, status=status.HTTP_400_BAD_REQUEST)
        if not file.content_type.startswith("image/"):
            return Response(
                {"detail": "Only image files are supported."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ext = Path(file.name or "").suffix.lower() or ".png"
        day = timezone.now().strftime("%Y/%m/%d")
        name = f"uploads/{day}/{get_random_string(16)}{ext}"
        path = default_storage.save(name, file)
        url = request.build_absolute_uri(f"{settings.MEDIA_URL}{path}")
        return Response({"url": url, "path": path})


# ---- Analytics --------------------------------------------------------------


def _detect_device(user_agent: str) -> str:
    ua = user_agent.lower()
    if "ipad" in ua or "tablet" in ua or "kindle" in ua:
        return AnalyticsVisit.Device.TABLET
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return AnalyticsVisit.Device.MOBILE
    return AnalyticsVisit.Device.DESKTOP


class TrackVisitView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        path = (request.data.get("path") or "/")[:500]
        if path.startswith("/admin"):
            return Response(status=status.HTTP_204_NO_CONTENT)

        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        AnalyticsVisit.objects.create(
            path=path,
            referrer=(request.data.get("referrer") or "")[:500],
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=user_agent,
            device=_detect_device(user_agent),
            session_key=request.session.session_key or "",
            is_authenticated=request.user.is_authenticated,
        )
        return Response(status=status.HTTP_201_CREATED)


class HeartbeatView(views.APIView):
    """Periodic ping from the browser: accumulate page + section dwell time."""
    permission_classes = [AllowAny]

    def post(self, request):
        path = (request.data.get("path") or "/")[:500]
        if path.startswith("/admin"):
            return Response(status=status.HTTP_204_NO_CONTENT)

        duration = 0
        try:
            duration = max(0, min(int(request.data.get("duration_seconds") or 0), 3600))
        except (TypeError, ValueError):
            duration = 0

        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        session_key = request.session.session_key or ""
        now = timezone.now()

        session, created = PageSession.objects.get_or_create(
            session_key=session_key,
            path=path,
            defaults={
                "device": _detect_device(user_agent),
                "referrer": (request.data.get("referrer") or "")[:500],
                "ip_address": request.META.get("REMOTE_ADDR"),
                "entered_at": now,
                "last_active_at": now,
                "duration_seconds": duration,
            },
        )
        if not created:
            session.duration_seconds += duration
            session.last_active_at = now
            session.save(update_fields=["duration_seconds", "last_active_at"])

        for item in request.data.get("sections") or []:
            section = str(item.get("section") or "")[:120]
            if not section:
                continue
            sec_duration = 0
            try:
                sec_duration = max(0, min(int(item.get("seconds") or 0), 3600))
            except (TypeError, ValueError):
                sec_duration = 0
            eng, eng_created = SectionEngagement.objects.get_or_create(
                session_key=session_key,
                path=path,
                section=section,
                defaults={
                    "duration_seconds": sec_duration,
                    "views_count": 1,
                    "first_seen_at": now,
                    "last_active_at": now,
                },
            )
            if not eng_created:
                eng.duration_seconds += sec_duration
                eng.views_count += 1
                eng.last_active_at = now
                eng.save(update_fields=["duration_seconds", "views_count", "last_active_at"])

        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityLogView(views.APIView):
    """Log a single user action (CTA click, search, scroll depth, ...)."""
    permission_classes = [AllowAny]

    def post(self, request):
        path = (request.data.get("path") or "/")[:500]
        if path.startswith("/admin"):
            return Response(status=status.HTTP_204_NO_CONTENT)

        action = (request.data.get("action") or "unknown")[:60]
        ActivityLog.objects.create(
            session_key=request.session.session_key or "",
            path=path,
            action=action,
            label=(request.data.get("label") or "")[:255],
            meta=request.data.get("meta") or {},
        )
        return Response(status=status.HTTP_201_CREATED)


class DashboardStatsView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        today = now.date()
        last_7 = now - timedelta(days=7)
        last_14 = now - timedelta(days=14)
        last_30 = now - timedelta(days=30)

        visits = AnalyticsVisit.objects.filter(viewed_at__gte=last_30)
        unique_sessions = visits.exclude(session_key="").values("session_key").distinct().count()

        by_day = (
            AnalyticsVisit.objects.filter(viewed_at__gte=last_14)
            .annotate(day=TruncDate("viewed_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        top_pages = (
            visits.values("path").annotate(count=Count("id")).order_by("-count")[:8]
        )

        devices = dict(
            visits.values_list("device")
            .annotate(count=Count("id"))
            .values_list("device", "count")
        )

        recent_leads = Lead.objects.order_by("-created_at")[:6]
        recent_visits = AnalyticsVisit.objects.order_by("-viewed_at")[:8]

        page_sessions = PageSession.objects.filter(last_active_at__gte=last_30)
        pages_time = (
            page_sessions.values("path")
            .annotate(
                sessions=Count("id"),
                total_seconds=Sum("duration_seconds"),
            )
            .order_by("-total_seconds")[:10]
        )

        section_rows = (
            SectionEngagement.objects.filter(last_active_at__gte=last_30)
            .values("path", "section")
            .annotate(
                views=Sum("views_count"),
                total_seconds=Sum("duration_seconds"),
            )
            .order_by("-total_seconds")
        )
        sections_by_page: dict = {}
        for row in section_rows:
            sections_by_page.setdefault(row["path"], []).append(
                {
                    "section": row["section"],
                    "views": row["views"],
                    "total_seconds": row["total_seconds"] or 0,
                }
            )

        recent_activity = ActivityLog.objects.order_by("-created_at")[:20]

        active_now = (
            PageSession.objects.filter(last_active_at__gte=now - timedelta(minutes=5))
            .values("path")
            .annotate(active=Count("id"))
            .order_by("-active")
        )

        return Response(
            {
                "counts": {
                    "products": Product.objects.count(),
                    "solutions": Solution.objects.count(),
                    "articles": Article.objects.count(),
                    "case_studies": CaseStudy.objects.count(),
                    "testimonials": Testimonial.objects.count(),
                    "industries": Industry.objects.count(),
                    "universities": University.objects.count(),
                    "team": TeamMember.objects.count(),
                    "faqs": FAQ.objects.count(),
                    "leads": Lead.objects.count(),
                    "unread_leads": Lead.objects.filter(is_read=False).count(),
                    "archived_leads": Lead.objects.filter(is_archived=True).count(),
                    "hackathons": Hackathon.objects.count(),
                },
                "visits": {
                    "total_30d": visits.count(),
                    "unique_sessions_30d": unique_sessions,
                    "today": AnalyticsVisit.objects.filter(viewed_at__date=today).count(),
                    "last_7d": AnalyticsVisit.objects.filter(viewed_at__gte=last_7).count(),
                    "by_day": [
                        {"date": d["day"].isoformat(), "count": d["count"]} for d in by_day
                    ],
                    "top_pages": list(top_pages),
                    "devices": devices,
                },
                "engagement": {
                    "pages_time": [
                        {
                            "path": p["path"],
                            "sessions": p["sessions"],
                            "total_seconds": p["total_seconds"] or 0,
                            "avg_seconds": round(
                                (p["total_seconds"] or 0) / max(1, p["sessions"])
                            ),
                        }
                        for p in pages_time
                    ],
                    "sections_by_page": sections_by_page,
                    "recent_activity": [
                        {
                            "id": a.id,
                            "action": a.action,
                            "label": a.label,
                            "path": a.path,
                            "meta": a.meta,
                            "created_at": a.created_at.isoformat(),
                        }
                        for a in recent_activity
                    ],
                    "active_now": list(active_now),
                },
                "recent_leads": [
                    {
                        "id": l.id,
                        "name": l.name,
                        "category": l.category,
                        "organization": l.organization,
                        "email": l.email,
                        "phone": l.phone,
                        "industry": l.industry,
                        "need": l.need,
                        "budget_range": l.budget_range,
                        "message": l.message,
                        "status": l.status,
                        "source": l.source,
                        "is_read": l.is_read,
                        "is_archived": l.is_archived,
                        "lead_score": l.lead_score,
                        "created_at": l.created_at.isoformat(),
                    }
                    for l in recent_leads
                ],
                "recent_visits": VisitSerializer(recent_visits, many=True).data,
                "lead_statuses": dict(
                    Lead.objects.values_list("status")
                    .annotate(count=Count("id"))
                    .values_list("status", "count")
                ),
            }
        )


class AdminAuditListView(views.APIView):
    """Readable staff activity trail — who did what, when."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = AdminAudit.objects.select_related("actor").all()
        action = request.query_params.get("action")
        resource = request.query_params.get("resource")
        if action:
            qs = qs.filter(action=action)
        if resource:
            qs = qs.filter(resource=resource)
        return Response(AdminAuditSerializer(qs[:200], many=True).data)


class SiteConfigAdminView(views.APIView):
    """Singleton site settings — GET to read, PUT to update."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(SiteConfigAdminSerializer(SiteConfig.load()).data)

    def put(self, request):
        serializer = SiteConfigAdminSerializer(
            SiteConfig.load(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminTestEmailView(views.APIView):
    """Send a test email through the Brevo transactional API."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        ready = email_configured()
        return Response(
            {
                "configured": ready,
                "mode": "api" if getattr(settings, "BREVO_API_KEY", "") else "smtp",
                "host": settings.EMAIL_HOST,
                "port": settings.EMAIL_PORT,
                "from_email": settings.DEFAULT_FROM_EMAIL,
                "from_name": settings.DEFAULT_FROM_NAME,
            }
        )

    def post(self, request):
        to = (request.data.get("to") or "").strip()
        if not to:
            return Response({"detail": "Provide a recipient email address."}, status=400)
        if not email_configured():
            return Response(
                {
                    "detail": "No Brevo key configured. Add BREVO_API_KEY (API key) or EMAIL_HOST_USER + EMAIL_HOST_PASSWORD (SMTP key) to backend/.env."
                },
                status=400,
            )
        subject = "Brevo test email — Florante"
        body = (
            "Hello,\n\n"
            "This is a test email sent through the Brevo transactional API configured "
            "for the Florante site. If you received this, email replies are fully working.\n\n"
            "— Florante Tech"
        )
        ok, detail = send_brevo_email(to, subject, body)
        if not ok:
            return Response({"detail": f"Email could not be sent: {detail}"}, status=400)
        _audit(
            request.user,
            AdminAudit.Action.SENT_TEST,
            "site",
            summary=f"Sent test email to {to}",
            meta={"channel": "brevo_api", "to": to},
        )
        return Response({"detail": f"Test email sent to {to}. {detail}"})


class TelegramWebhookView(views.APIView):
    """Public webhook — Telegram posts inbound messages here."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        secret = request.query_params.get("secret", "") or request.META.get("HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN", "")
        if settings.TELEGRAM_WEBHOOK_SECRET and secret != settings.TELEGRAM_WEBHOOK_SECRET:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        lead = tg.handle_update(request.data)
        if lead is not None:
            _audit(
                None,
                AdminAudit.Action.CREATED,
                "leads",
                lead,
                summary=f"Telegram message from {lead.name} (@{lead.telegram_username})",
                meta={"channel": "telegram", "chat_id": lead.telegram_chat_id},
            )
        return Response(status=status.HTTP_200_OK)


class AdminTelegramView(views.APIView):
    """Status + webhook management for the Telegram bot."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        me, err = tg.get_me() if tg.bot_ready() else (None, "")
        if not tg.bot_ready():
            return Response(
                {"configured": False, "username": "", "webhook_set": False, "detail": "Add TELEGRAM_BOT_TOKEN to backend/.env."}
            )
        return Response(
            {
                "configured": True,
                "username": (me or {}).get("username", "") if not err else "",
                "name": (me or {}).get("first_name", "") if not err else "",
                "webhook_set": False,
                "detail": err or "",
            }
        )

    def post(self, request):
        if not tg.bot_ready():
            return Response({"detail": "Add TELEGRAM_BOT_TOKEN to backend/.env."}, status=400)
        domain = getattr(settings, "SITE_DOMAIN", "localhost:8000")
        url = f"https://{domain}/api/telegram/webhook/"
        ok, detail = tg.set_webhook(url, settings.TELEGRAM_WEBHOOK_SECRET or None)
        if not ok:
            return Response({"detail": detail}, status=400)
        return Response({"detail": detail, "webhook_set": True})


class AdminUserListView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.order_by("username").values(
            "id", "username", "email", "first_name", "last_name",
            "is_staff", "is_superuser", "is_active", "date_joined", "last_login",
        )
        return Response(list(users))

    def post(self, request):
        email = (request.data.get("email") or "").strip()
        name = (request.data.get("name") or request.data.get("username") or "").strip()
        password = request.data.get("password", "")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email__iexact=email).exists():
            return Response(
                {"detail": "A user with this email address already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = name.lower().replace(" ", "_") if name else email.split("@")[0]
        if User.objects.filter(username=username).exists():
            username = f"{username}_{get_random_string(4)}"

        first_name = name.split()[0] if name else ""
        last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        _audit(
            request.user,
            AdminAudit.Action.CREATED,
            "users",
            user,
            summary=f"Registered new admin: {email} ({user.username})",
        )

        return Response(
            {
                "detail": f"Admin user '{user.username}' created successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_staff": user.is_staff,
                    "is_active": user.is_active,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class AdminUserDetailView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        """Return full profile for a single admin user."""
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "id": target_user.id,
            "username": target_user.username,
            "email": target_user.email,
            "first_name": target_user.first_name,
            "last_name": target_user.last_name,
            "is_staff": target_user.is_staff,
            "is_superuser": target_user.is_superuser,
            "is_active": target_user.is_active,
            "date_joined": target_user.date_joined,
            "last_login": target_user.last_login,
        })

    def patch(self, request, pk):
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Superusers are protected — cannot be deactivated
        if target_user.is_superuser:
            return Response(
                {"detail": "Superuser accounts cannot be deactivated."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Admins cannot deactivate themselves
        if target_user.id == request.user.id:
            return Response(
                {"detail": "You cannot deactivate your own account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "is_active" in request.data:
            is_active = bool(request.data["is_active"])
            target_user.is_active = is_active
            target_user.save(update_fields=["is_active"])

            if not is_active:
                Token.objects.filter(user=target_user).delete()

            _audit(
                request.user,
                AdminAudit.Action.UPDATED,
                "users",
                target_user,
                summary=f"{'Deactivated' if not is_active else 'Reactivated'} admin user '{target_user.username}'",
            )

        return Response(
            {
                "id": target_user.id,
                "username": target_user.username,
                "email": target_user.email,
                "is_active": target_user.is_active,
            }
        )

    def delete(self, request, pk):
        try:
            target_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Superusers are protected — cannot be deleted
        if target_user.is_superuser:
            return Response(
                {"detail": "Superuser accounts cannot be deleted."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Admins cannot delete themselves
        if target_user.id == request.user.id:
            return Response(
                {"detail": "You cannot delete your own account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = target_user.username
        Token.objects.filter(user=target_user).delete()
        target_user.delete()

        _audit(
            request.user,
            AdminAudit.Action.DELETED,
            "users",
            resource_id=pk,
            summary=f"Deleted admin user '{username}'",
        )

        return Response({"detail": f"Admin user '{username}' has been deleted."})


# ---- Admin CRUD viewsets (registered in urls) -------------------------------


class ProductAdminViewSet(AdminCRUDViewSet):
    resource_key = "products"
    queryset = Product.objects.all()
    serializer_class = ProductAdminSerializer
    search_fields = ["name", "category"]


class SolutionAdminViewSet(AdminCRUDViewSet):
    resource_key = "solutions"
    queryset = Solution.objects.all()
    serializer_class = SolutionAdminSerializer
    search_fields = ["title", "category"]


class ArticleAdminViewSet(AdminCRUDViewSet):
    resource_key = "articles"
    queryset = Article.objects.all()
    serializer_class = ArticleAdminSerializer
    search_fields = ["title", "category"]


class CaseStudyAdminViewSet(AdminCRUDViewSet):
    resource_key = "case-studies"
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudyAdminSerializer
    search_fields = ["title", "client"]


class IndustryAdminViewSet(AdminCRUDViewSet):
    resource_key = "industries"
    queryset = Industry.objects.all()
    serializer_class = IndustryAdminSerializer
    search_fields = ["name"]


class TestimonialAdminViewSet(AdminCRUDViewSet):
    resource_key = "testimonials"
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialAdminSerializer
    search_fields = ["author", "company"]


class UniversityAdminViewSet(AdminCRUDViewSet):
    resource_key = "universities"
    queryset = University.objects.all()
    serializer_class = UniversityAdminSerializer
    search_fields = ["name", "county"]


class TeamMemberAdminViewSet(AdminCRUDViewSet):
    resource_key = "team"
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberAdminSerializer
    search_fields = ["name", "role"]


class FAQAdminViewSet(AdminCRUDViewSet):
    resource_key = "faqs"
    queryset = FAQ.objects.all()
    serializer_class = FAQAdminSerializer
    search_fields = ["question", "context"]


class LeadAdminViewSet(AdminCRUDViewSet):
    resource_key = "leads"
    queryset = Lead.objects.all()
    serializer_class = LeadAdminSerializer
    search_fields = ["name", "email", "organization"]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        read = params.get("read")
        archived = params.get("archived")
        email = params.get("email")
        if read is not None:
            qs = qs.filter(is_read=read.lower() in ("1", "true", "yes"))
        if archived is not None:
            qs = qs.filter(is_archived=archived.lower() in ("1", "true", "yes"))
        if email:
            qs = qs.filter(email__iexact=email)
        return qs

    @action(detail=False, methods=["get"])
    def senders(self, request):
        """Who has messaged us — aggregated by email with counts."""
        rows = (
            Lead.objects.exclude(email="")
            .values("email")
            .annotate(count=Count("id"), last=Max("created_at"), name=Max("name"))
            .order_by("-count")
        )
        return Response(list(rows))

    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        lead = self.get_object()
        is_read = bool(request.data.get("is_read", True))
        lead.is_read = is_read
        lead.save(update_fields=["is_read", "updated_at"])
        _audit(
            request.user,
            AdminAudit.Action.MARKED_READ if is_read else AdminAudit.Action.MARKED_UNREAD,
            "leads",
            lead,
            summary=f"{'Marked read' if is_read else 'Marked unread'}: {lead.name}",
        )
        return Response({"is_read": lead.is_read})

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        lead = self.get_object()
        is_archived = bool(request.data.get("is_archived", True))
        lead.is_archived = is_archived
        lead.save(update_fields=["is_archived", "updated_at"])
        _audit(
            request.user,
            AdminAudit.Action.ARCHIVED if is_archived else AdminAudit.Action.UNARCHIVED,
            "leads",
            lead,
            summary=f"{'Archived' if is_archived else 'Restored'}: {lead.name}",
        )
        return Response({"is_archived": lead.is_archived})

    @action(detail=True, methods=["post"])
    def reply(self, request, pk=None):
        """Reply to a message — email via Brevo or Telegram via the bot."""
        lead = self.get_object()
        channel = (request.data.get("channel") or "email").lower()
        subject = (request.data.get("subject") or "").strip()
        body = (request.data.get("body") or "").strip()

        if channel == "telegram":
            if not lead.telegram_chat_id:
                return Response(
                    {"detail": "This message has no Telegram chat to reply to."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not body:
                return Response({"detail": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)
            ok, detail = tg.send_message(lead.telegram_chat_id, body)
            if not ok:
                return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)
            lead.is_read = True
            if lead.status == Lead.Status.NEW:
                lead.status = Lead.Status.CONTACTED
            lead.save(update_fields=["is_read", "status", "updated_at"])
            _audit(
                request.user,
                AdminAudit.Action.SENT_TELEGRAM,
                "leads",
                lead,
                summary=f"Replied to {lead.name} via Telegram (@{lead.telegram_username})",
                meta={"channel": "telegram", "chat_id": lead.telegram_chat_id, "body": body},
            )
            return Response({"detail": "Reply sent via Telegram.", "delivered": True})

        if channel != "email":
            return Response({"detail": "Only email and telegram replies are supported."}, status=400)
        if not lead.email:
            return Response({"detail": "This message has no email address to reply to."}, status=400)
        if not subject or not body:
            return Response({"detail": "Subject and message are required."}, status=400)

        brevo_ready_flag = email_configured()
        from_addr = settings.DEFAULT_FROM_EMAIL or "techrica2@gmail.com"
        meta = {"channel": channel, "to": lead.email, "subject": subject, "body": body}

        if brevo_ready_flag:
            ok, detail = send_brevo_email(lead.email, subject, body)
            if not ok:
                return Response(
                    {"detail": f"Email could not be sent: {detail}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            lead.is_read = True
            if lead.status == Lead.Status.NEW:
                lead.status = Lead.Status.CONTACTED
            lead.save(update_fields=["is_read", "status", "updated_at"])
            _audit(
                request.user,
                AdminAudit.Action.REPLIED,
                "leads",
                lead,
                summary=f"Replied to {lead.name} via Email ({lead.email})",
                meta=meta,
            )
            return Response({"detail": "Reply sent.", "delivered": True})

        url = f"mailto:{lead.email}?subject={quote(subject)}&body={quote(body)}"
        _audit(
            request.user,
            AdminAudit.Action.REPLIED,
            "leads",
            lead,
            summary=f"Replied to {lead.name} via Email ({lead.email})",
            meta={**meta, "fallback": True},
        )
        return Response(
            {"detail": "Email is not configured yet — opening your mail app instead.", "delivered": False, "url": url}
        )


class HackathonAdminViewSet(AdminCRUDViewSet):
    resource_key = "hackathons"
    queryset = Hackathon.objects.all()
    serializer_class = HackathonAdminSerializer
    search_fields = ["title", "status"]


ADMIN_VIEWSETS = {
    "products": ProductAdminViewSet,
    "solutions": SolutionAdminViewSet,
    "articles": ArticleAdminViewSet,
    "case-studies": CaseStudyAdminViewSet,
    "industries": IndustryAdminViewSet,
    "testimonials": TestimonialAdminViewSet,
    "universities": UniversityAdminViewSet,
    "team": TeamMemberAdminViewSet,
    "faqs": FAQAdminViewSet,
    "leads": LeadAdminViewSet,
    "hackathons": HackathonAdminViewSet,
}
