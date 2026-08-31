from django.core.management.base import BaseCommand
from apps.products.models import Product
from apps.cms.models import Industry

PRODUCTS = [
    {
        "name": "Unicrib Accommodation System",
        "slug": "unicrib",
        "category": "Education Technology",
        "short_description": "Automated student housing, room allocation, and fee management platform for African universities.",
        "long_description": "Unicrib simplifies campus accommodation by digitizing room reservation, fee verification, student check-in, and maintenance ticketing in one seamless portal. Built for African university realities — including M-Pesa payment verification, multi-building room maps, and offline-resilient check-in terminals.",
        "features": [
            "Online Room Booking & Instant Allocation",
            "Automated M-Pesa Fee Verification",
            "Digital Student Pass & Check-In",
            "Maintenance Request & Tracking System",
            "Occupancy Reports & Admin Dashboard",
            "Multi-building & Multi-campus Support",
        ],
        "benefits": [
            "Zero queue lines during admission week",
            "Eliminate fee record reconciliation errors",
            "Real-time occupancy tracking for campus admin",
            "Reduce housing office workload by 70%",
        ],
        "pricing": "Custom quote",
        "pricing_type": "custom",
        "demo_url": "/contact",
        "status": "available",
        "technologies": ["React", "Django", "PostgreSQL", "M-Pesa Daraja API", "Redis"],
        "integrations": ["M-Pesa", "Google Workspace", "SMS Gateways", "University ERP"],
        "faqs": [
            {"question": "Can Unicrib integrate with our existing ERP?", "answer": "Yes, Unicrib provides REST APIs to sync student databases and financial ledgers seamlessly with any ERP system."},
            {"question": "How fast can we deploy Unicrib?", "answer": "Setup and data migration typically take under 2 weeks for university campuses of any size."},
            {"question": "Does it work during internet outages?", "answer": "The check-in terminal caches student passes locally and syncs automatically when connectivity resumes."},
        ],
        "target_customer": "Universities, polytechnics, and private student hostels.",
        "problem_solved": "Eliminates long physical registration queues and manual payment verification spreadsheets during semester intake.",
        "how_it_works": "Students log in, view available rooms in real time, pay via M-Pesa or bank integration, and receive an instant digital hostel gate pass. Admin staff monitor occupancy and payments from a live dashboard.",
        "security_notes": "Built with role-based access control (RBAC), encrypted student records, and full payment audit trails compliant with Kenya DPA requirements.",
        "published": True,
        "industry_slugs": ["education"],
    },
    {
        "name": "Florante Core ERP",
        "slug": "florante-core-erp",
        "category": "SME Solutions",
        "short_description": "All-in-one business management software for sales, inventory, accounting, and staff management.",
        "long_description": "Engineered specifically for growing African businesses to automate invoicing, track inventory in real time, and monitor company performance from any device. Florante Core ERP replaces the chaos of spreadsheets and paper receipts with structured, tamper-proof business records — without the enterprise price tag.",
        "features": [
            "Real-time Inventory & Stock Tracking",
            "Automated Tax Invoice Generation",
            "Point of Sale (POS) Integration",
            "Multi-branch Financial Auditing",
            "Staff Management & Attendance",
            "M-Pesa & Bank Reconciliation",
        ],
        "benefits": [
            "Full control over stock theft and discrepancies",
            "Instant daily financial summaries via mobile",
            "Multi-branch oversight from a single dashboard",
            "KRA-compliant invoice and tax reporting",
        ],
        "pricing": "KES 5,000 / month",
        "pricing_type": "monthly",
        "demo_url": "/contact",
        "status": "available",
        "technologies": ["TypeScript", "React", "Python", "Django", "PostgreSQL", "Tailwind CSS"],
        "integrations": ["M-Pesa Daraja API", "KRA iTax", "WhatsApp Notifications", "Email Reports"],
        "faqs": [
            {"question": "Does it work offline?", "answer": "Yes, the POS module caches transactions locally and syncs automatically when connection resumes."},
            {"question": "Can it handle multiple branches?", "answer": "Yes, Florante Core ERP supports unlimited branches with consolidated reporting visible to HQ in real time."},
            {"question": "Is there a setup fee?", "answer": "There is a one-time onboarding and data migration fee. Monthly billing begins after go-live."},
        ],
        "target_customer": "Retailers, wholesalers, logistics firms, and growing service businesses.",
        "problem_solved": "Replaces unorganized paper receipts and Excel files with automated, tamper-proof business records and real-time financial visibility.",
        "how_it_works": "Staff record sales or inventory changes via the POS or web interface. The system automatically adjusts financial ledgers, generates KRA-compliant invoices, and sends automated summaries to management every day.",
        "security_notes": "Includes comprehensive audit trail logging for every stock movement and financial transaction. Role-based permissions prevent unauthorized access to sensitive financial data.",
        "published": True,
        "industry_slugs": ["smes", "financial-services"],
    },
    {
        "name": "Sentinel Security Audit Suite",
        "slug": "sentinel-audit",
        "category": "Cybersecurity",
        "short_description": "Automated vulnerability scanner, API security monitor, and threat detection tool for web and cloud applications.",
        "long_description": "Sentinel continuously audits web endpoints, databases, and microservices for security flaws, compliance gaps, and unauthorized access attempts — giving your security team real-time visibility without waiting for an annual penetration test.",
        "features": [
            "Automated OWASP Vulnerability Scanning",
            "Continuous API Access Monitoring",
            "ISO 27001 Compliance Checking",
            "Real-Time Threat Alerts via Slack & Email",
            "Scheduled & On-Demand Penetration Testing",
            "Executive Security Reports",
        ],
        "benefits": [
            "Identify security weaknesses before attackers do",
            "Continuous compliance with Kenya Data Protection Regulations",
            "Automated vulnerability reports for board-level review",
            "Reduce breach response time from hours to minutes",
        ],
        "pricing": "Custom quote",
        "pricing_type": "custom",
        "demo_url": "/contact",
        "status": "available",
        "technologies": ["Python", "Docker", "Go", "PostgreSQL", "OWASP ZAP", "Burp Suite"],
        "integrations": ["Slack Alerts", "Email / SMS Gateways", "GitHub CI/CD", "Jira"],
        "faqs": [
            {"question": "Can Sentinel audit third-party APIs?", "answer": "Yes, Sentinel supports authenticated and unauthenticated API vulnerability assessments against any HTTP/HTTPS endpoint."},
            {"question": "Will the scans disrupt our live services?", "answer": "Sentinel operates in passive monitoring mode by default. Active penetration scans are scheduled during off-peak hours."},
            {"question": "Does it help with DPA compliance?", "answer": "Yes, Sentinel includes a dedicated Kenya Data Protection Act compliance module that maps findings directly to regulatory requirements."},
        ],
        "target_customer": "Banks, SACCOs, fintech startups, hospitals, and government digital services.",
        "problem_solved": "Prevents data breaches and costly regulatory fines by detecting vulnerabilities proactively instead of reacting after an incident.",
        "how_it_works": "Sentinel runs scheduled or continuous security scans against your specified endpoints and outputs a risk-prioritized remediation report with severity scores and step-by-step fix instructions.",
        "security_notes": "Operates with zero data exposure, running entirely within isolated secure execution environments. No customer data leaves your infrastructure.",
        "published": True,
        "industry_slugs": ["financial-services", "organizations"],
    },
    {
        "name": "Flow Forms & Workflow Digitizer",
        "slug": "flow-forms",
        "category": "Organizations",
        "short_description": "Paperless form builder, approval engine, and document tracking portal for enterprises and NGOs.",
        "long_description": "Replace physical sign-off sheets, requisition forms, and email approval threads with structured, automated digital workflows. Flow Forms gives organizations complete visibility over every pending approval, from travel requests to procurement sign-offs, with a full tamper-proof audit trail.",
        "features": [
            "Drag-and-Drop Digital Form Builder",
            "Multi-Tier Approval Routing",
            "E-Signature & Timestamp Audit Trail",
            "PDF Report Generation & Export",
            "WhatsApp & Email Approval Notifications",
            "Role-based Access Control",
        ],
        "benefits": [
            "Cut approval turnaround time from days to minutes",
            "100% paperless institutional record keeping",
            "Never lose a pending document or requisition again",
            "Full audit trail for board and donor reporting",
        ],
        "pricing": "KES 15,000 / month",
        "pricing_type": "monthly",
        "demo_url": "/contact",
        "status": "available",
        "technologies": ["React", "FastAPI", "PostgreSQL", "Celery", "Redis"],
        "integrations": ["Google Drive", "Microsoft 365", "WhatsApp Business API", "Email"],
        "faqs": [
            {"question": "Can non-technical staff create forms?", "answer": "Yes, the visual drag-and-drop form builder requires absolutely zero coding knowledge."},
            {"question": "How many approval levels can we configure?", "answer": "Flow Forms supports unlimited approval tiers with conditional routing based on form field values."},
            {"question": "Is the audit trail accepted by auditors?", "answer": "Yes, the audit log includes timestamps, user IDs, IP addresses, and digital signatures that satisfy both internal and external audit requirements."},
        ],
        "target_customer": "NGOs, government agencies, schools, hospitals, and corporate organizations.",
        "problem_solved": "Eliminates lost paperwork and slow manual approval chains that delay operations and frustrate staff across departments.",
        "how_it_works": "Staff submit digital forms via web or mobile. The system routes each submission automatically to the correct approvers, who receive a WhatsApp or email notification and approve with one click.",
        "security_notes": "All approvals are cryptographically signed with date, time, user identity, and IP address audit logs that cannot be altered after submission.",
        "published": True,
        "industry_slugs": ["organizations", "smes"],
    },
]


class Command(BaseCommand):
    help = "Seed product records into the database"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in PRODUCTS:
            industry_slugs = data.pop("industry_slugs", [])
            obj, was_created = Product.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            # Attach industries
            industries = Industry.objects.filter(slug__in=industry_slugs)
            obj.industries.set(industries)

            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {obj.name}"))
            else:
                updated += 1
                self.stdout.write(f"  Updated: {obj.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created} created, {updated} updated. Total products: {Product.objects.count()}"
            )
        )
