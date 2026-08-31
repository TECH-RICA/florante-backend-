from django.core.management.base import BaseCommand
from apps.cms.models import Industry

INDUSTRIES = [
    {
        "name": "Education",
        "slug": "education",
        "short_description": "Technology solutions for universities, colleges, schools, and EdTech platforms.",
        "description": (
            "We build platforms that help universities, colleges, and schools deliver better education, "
            "manage operations, and connect students with opportunities. From student management systems "
            "and digital accommodation platforms to learning management tools and alumni engagement portals, "
            "Florante powers the modern African campus."
        ),
        "featured": True,
        "published": True,
    },
    {
        "name": "SMEs",
        "slug": "smes",
        "short_description": "Affordable automation and digital tools for small and growing African businesses.",
        "description": (
            "We help small and growing businesses automate operations, build digital presence, and compete "
            "in an increasingly digital marketplace. Our ERP systems, invoicing tools, inventory trackers, "
            "and workflow automation products are built specifically for the pace and budget realities of "
            "African SMEs."
        ),
        "featured": True,
        "published": True,
    },
    {
        "name": "Financial Services",
        "slug": "financial-services",
        "short_description": "Secure, compliant technology for banks, SACCOs, fintechs, and microfinance institutions.",
        "description": (
            "We build secure, compliant technology for financial institutions — from mobile money integrations "
            "to fraud detection systems. Our solutions address loan management, M-Pesa integration, regulatory "
            "compliance dashboards, and digital customer onboarding for banks, SACCOs, and fintech startups "
            "operating across East Africa."
        ),
        "featured": True,
        "published": True,
    },
    {
        "name": "Organizations",
        "slug": "organizations",
        "short_description": "Digital transformation tools for NGOs, government agencies, and enterprises.",
        "description": (
            "We support NGOs, government agencies, and enterprises in digitizing workflows, managing projects, "
            "and improving organizational efficiency. Our tools replace paper-based processes with structured "
            "digital approval flows, impact reporting dashboards, and staff management systems built for "
            "multi-branch African institutions."
        ),
        "featured": True,
        "published": True,
    },
]


class Command(BaseCommand):
    help = "Seed industry records into the database"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in INDUSTRIES:
            obj, was_created = Industry.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {obj.name}"))
            else:
                updated += 1
                self.stdout.write(f"  Updated: {obj.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created} created, {updated} updated. Total industries: {Industry.objects.count()}"
            )
        )
