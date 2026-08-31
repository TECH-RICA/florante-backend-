from django.core.management.base import BaseCommand
from apps.insights.models import CaseStudy
from apps.cms.models import Industry

CASE_STUDIES = [
    {
        "title": "Digitizing Campus Accommodation for 15,000+ Students",
        "slug": "unicrib-campus-deployment",
        "client": "East African Partner Universities",
        "industry_slug": "education",
        "challenge": "Long physical queues during registration week, payment verification discrepancies, and rooms being double-allocated due to manual ledger management.",
        "existing_situation": "Manual ledger books and Excel spreadsheets managed by overwhelmed housing officers during peak admission periods. Fee clearance required students to visit multiple offices across campus, with reconciliation errors causing disputes.",
        "solution": "Deployed the Unicrib Accommodation Platform with automated M-Pesa fee verification, real-time room availability mapping, and instant digital gate pass generation.",
        "technologies": ["React", "Django", "PostgreSQL", "M-Pesa Daraja API", "Redis"],
        "implementation": "Phased rollout over 2 weeks across multi-building student hostelling complexes. Staff trained in parallel. Legacy data migrated from Excel with automated validation checks.",
        "result": "Eliminated physical admission queues entirely. Fee verification time reduced from 2–3 days to under 3 seconds. Housing officer productivity increased by 4x. Zero double-allocation incidents recorded.",
        "client_quote": "Florante transformed our hostel administration from a week of chaos into a smooth digital experience. Students can now allocate and pay for their room before they even leave home.",
        "client_quote_author": "Dean of Student Affairs",
        "published": True,
    },
    {
        "title": "ISO Security Hardening & Continuous Vulnerability Monitoring",
        "slug": "sentinel-cybersecurity-banking",
        "client": "Regional Financial Institution",
        "industry_slug": "financial-services",
        "challenge": "Meeting strict Kenya Data Protection Act compliance requirements while securing multi-branch financial APIs against an increasing threat surface.",
        "existing_situation": "Periodic manual security audits left system endpoints exposed to emerging cyber threats between audit cycles. No real-time visibility into unauthorized access attempts. Regulatory examiners flagged security gaps during CBK inspection.",
        "solution": "Integrated the Sentinel Security Audit Suite for 24/7 endpoint vulnerability scanning, continuous API access monitoring, and automated compliance reporting aligned to Kenya DPA and ISO 27001.",
        "technologies": ["Python", "Docker", "WAF", "PostgreSQL", "OWASP ZAP"],
        "implementation": "Non-disruptive agentless deployment scanning core API gateways and database endpoints continuously without requiring any changes to existing infrastructure.",
        "result": "Achieved 100% regulatory data privacy compliance at the next CBK inspection. Zero high-severity vulnerabilities outstanding within 30 days of deployment. Security team response time to incidents reduced from 6 hours to under 15 minutes.",
        "client_quote": "Sentinel gives our board complete visibility over system security and compliance status. We no longer wait for the annual audit to find out if we have problems.",
        "client_quote_author": "Head of IT Infrastructure",
        "published": True,
    },
    {
        "title": "End-to-End Procurement Digitization for a Pan-African NGO",
        "slug": "flow-forms-ngo-procurement",
        "client": "Pan-African Development NGO",
        "industry_slug": "organizations",
        "challenge": "Procurement approval cycles averaging 5 days due to paper requisition forms being physically routed between field offices and Nairobi headquarters.",
        "existing_situation": "Paper-based purchase orders, travel requests, and expense claims routed by courier and WhatsApp photo between 12 country offices. Forms regularly lost. Donor audits required weeks of manual file retrieval.",
        "solution": "Deployed Flow Forms & Workflow Digitizer with custom multi-tier approval routing, e-signature capture, and a centralized institutional document archive linked to the procurement ERP.",
        "technologies": ["React", "FastAPI", "PostgreSQL", "Celery", "WhatsApp Business API"],
        "implementation": "Configured in 3 weeks with staff training delivered remotely across all 12 country offices. Legacy paper forms digitized and archived. Approval routing rules configured by the client's own operations team.",
        "result": "Procurement approval cycle reduced from 5 days to under 4 hours. Zero lost documents since deployment. Donor audit preparation time reduced from 3 weeks to 2 days.",
        "client_quote": "Our field teams no longer wait days for Nairobi to approve a KES 5,000 purchase. The whole organization moves faster now.",
        "client_quote_author": "Operations Director",
        "published": True,
    },
    {
        "title": "Multi-Branch ERP Deployment for a Growing Wholesale Distributor",
        "slug": "core-erp-wholesale-sme",
        "client": "Kenya Wholesale Distribution Business",
        "industry_slug": "smes",
        "challenge": "Stock theft, unreconciled inventory discrepancies, and no real-time visibility into the performance of three branches spread across Central Kenya.",
        "existing_situation": "Branch managers maintained separate Excel inventory files emailed to head office weekly. Reconciliation took 3 days each month. Stock discrepancies of 8–12% were recorded but unresolvable.",
        "solution": "Deployed Florante Core ERP across all three branches with centralized real-time inventory tracking, automated daily financial summaries, and a manager-level mobile dashboard.",
        "technologies": ["React", "Django", "PostgreSQL", "M-Pesa Daraja API", "Redis"],
        "implementation": "Go-live in 10 days. Historical stock data migrated from Excel. Branch staff trained on-site in one day per location. M-Pesa reconciliation configured for paybill and till accounts.",
        "result": "Stock discrepancies dropped by 90% within the first month. Monthly reconciliation now runs automatically overnight. Managing Director reviews all three branch financials from a single mobile dashboard every morning.",
        "client_quote": "I used to spend every Monday morning driving between branches to chase numbers. Now I open my phone at 7am and everything is already there.",
        "client_quote_author": "Managing Director",
        "published": True,
    },
]


class Command(BaseCommand):
    help = "Seed case study records into the database"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in CASE_STUDIES:
            industry_slug = data.pop("industry_slug", None)
            industry = Industry.objects.filter(slug=industry_slug).first() if industry_slug else None
            data["industry"] = industry

            obj, was_created = CaseStudy.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {obj.title[:60]}"))
            else:
                updated += 1
                self.stdout.write(f"  Updated: {obj.title[:60]}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created} created, {updated} updated. Total case studies: {CaseStudy.objects.count()}"
            )
        )
