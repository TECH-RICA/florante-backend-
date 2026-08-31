from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from apps.insights.models import Article

ARTICLES = [
    {
        "title": "The Rise of Pragmatic AI in African Enterprise Operations",
        "slug": "ai-trends-africa-2026",
        "category": "ai",
        "excerpt": "How forward-thinking African businesses are deploying targeted machine learning models to solve operational bottlenecks rather than chasing hype.",
        "content": """Artificial Intelligence in Africa has reached an inflection point. While global headlines focus on multi-billion dollar general language models, African enterprises and tech teams are quietly building pragmatic, domain-focused AI systems that solve real operational bottlenecks.

## Moving Beyond Generic Chatbots

Generic AI chatbots often fail when faced with local languages, specialized business jargon, or specific African regulatory environments. African organizations are moving toward fine-tuned, localized models that handle document extraction, M-Pesa transaction auditing, and dialect-aware customer service.

The most impactful implementations we have seen combine a narrow, well-defined problem scope with a clean dataset that reflects local operating conditions. A government agency using an AI model trained on Swahili service requests will outperform a general-purpose chatbot every time.

## Automated Operational Workflows

The biggest ROI for AI in East Africa today is in workflow automation. From automated invoice processing in SMEs to credit scoring models for micro-lenders, machine learning is reducing operational cycle times from days to seconds.

Key wins we are seeing across our client base:

- **Invoice and receipt automation** — extracting line items, VAT amounts, and supplier details with 95%+ accuracy.
- **Loan application screening** — reducing manual underwriter review time by 70% without sacrificing accuracy.
- **Fraud pattern detection** — flagging anomalous M-Pesa transactions in real time before settlement.

## What Separates Successful AI Projects

Three consistent factors appear in every successful AI deployment we have studied:

1. **Clear problem definition** — The team knows exactly what decision or task the AI will automate.
2. **Quality labeled data** — Messy, inconsistent data is the single biggest reason AI projects fail.
3. **Integration into existing workflows** — The AI output connects directly to the tools staff already use daily.

## Key Takeaway for Business Leaders

Building successful AI systems requires starting with a clear problem definition. Identify where your team spends manual hours, structure your data, and deploy targeted AI tools that integrate directly into your existing software stack. The era of AI for its own sake is over — the winners are organizations deploying AI that saves real money on Monday morning.""",
        "author_name": "Florante AI Research",
        "author_role": "Engineering Team",
        "tags": ["AI", "Automation", "Machine Learning", "Africa"],
        "featured_image": "",
        "is_featured": True,
        "is_published": True,
        "published_at": parse_datetime("2026-08-15T10:00:00Z"),
        "views_count": 342,
        "seo_title": "The Rise of Pragmatic AI in African Enterprise — Florante Insights",
        "seo_description": "How African businesses deploy targeted ML models to solve operational bottlenecks. Practical AI insights from Florante Tech.",
    },
    {
        "title": "Navigating Kenya's Data Protection Act for Digital Systems",
        "slug": "cybersecurity-compliance-kenya",
        "category": "cybersecurity",
        "excerpt": "A practical breakdown of data privacy requirements for software applications operating in Kenya and the wider East African region.",
        "content": """Compliance with data protection laws is no longer optional for African companies. Kenya's Data Protection Act (DPA) enforces strict guidelines on how personal data is collected, processed, and stored — with penalties for non-compliance that can reach millions of shillings.

## Who Does the DPA Apply To?

The Act applies to any organization that processes the personal data of individuals in Kenya, regardless of where the organization is headquartered. This includes banks, hospitals, universities, NGOs, SaaS platforms, and mobile applications.

## Data Minimization & Consent

Organizations must only collect data that is strictly required for the service rendered. Clear, informed user consent must be captured before collection and logged in audit trails. Pre-ticked checkboxes or bundled consent hidden in terms of service do not meet DPA standards.

Practical steps:

- Audit every form and API endpoint that collects user data.
- Implement explicit consent checkboxes with version-tracked privacy policy links.
- Store consent timestamps and user IDs in a tamper-proof consent ledger.

## Encryption & Access Control

All customer records, API keys, and financial credentials must be encrypted both in transit (TLS 1.3) and at rest (AES-256). Role-based access control (RBAC) ensures staff members only access data necessary for their specific role.

A developer should never have access to live customer financial records. A customer service agent should not see password hashes. Enforce least-privilege access across every system layer.

## Incident Response Requirements

In the event of a security breach or unauthorized access attempt, organizations are legally mandated to notify the Office of the Data Protection Commissioner (ODPC) and affected data subjects within 72 hours of becoming aware of the breach.

This makes proactive security logging non-negotiable. You cannot report what you cannot detect.

## Practical Compliance Roadmap

1. Conduct a data inventory — map every personal data field you store and why.
2. Appoint a Data Protection Officer (DPO) if you process data at scale.
3. Implement encryption, RBAC, and audit logging across all systems.
4. Draft and publish a compliant Privacy Policy and Cookie Policy.
5. Run a quarterly vulnerability assessment to catch new exposure points.

Florante provides full DPA gap analysis, remediation planning, and technical implementation for organizations seeking compliance.""",
        "author_name": "Florante Security Team",
        "author_role": "Cybersecurity Desk",
        "tags": ["Cybersecurity", "Compliance", "Privacy", "Kenya", "DPA"],
        "featured_image": "",
        "is_featured": False,
        "is_published": True,
        "published_at": parse_datetime("2026-08-10T14:30:00Z"),
        "views_count": 518,
        "seo_title": "Kenya Data Protection Act Compliance for Software — Florante Insights",
        "seo_description": "Practical guide to DPA compliance for Kenyan digital systems. Data minimization, encryption, and incident response requirements explained.",
    },
    {
        "title": "How African Institutions Are Replacing Paper Sheets with Digital Workflows",
        "slug": "paperless-workflows-ngos",
        "category": "digital-transformation",
        "excerpt": "A step-by-step guide to digitizing approval flows, paper forms, and departmental requests without disrupting staff operations.",
        "content": """Transitioning an institution from physical paper files to digital workflows is a strategic shift that transforms organizational speed and accountability. But done poorly, it creates confusion, staff resistance, and parallel paper-digital hybrid chaos that is worse than before.

Here is how high-performing African institutions are doing it right.

## Start With a Workflow Audit

Before touching any software, map every paper-based process in the organization. Travel request forms. Leave applications. Procurement requisitions. Inspection reports. Board approval sign-off sheets.

For each process, document:

- Who initiates it
- Every approval step and who is responsible
- How long it currently takes end-to-end
- Where it most often stalls or gets lost

This audit typically reveals that 80% of institutional bottlenecks come from just 20% of the workflows.

## Digital Forms & Conditional Logic

Replace paper sheets with responsive digital forms that validate input automatically. A leave request form should reject dates that fall on public holidays. A procurement form should flag requests above a budget threshold and route them to a different approver.

Conditional logic eliminates entire categories of manual back-and-forth between departments.

## Multi-Tier Approval Routing

Define the exact sign-off sequence digitally. When a requisition is submitted, the system routes it automatically to the line manager, then finance, then the director — each receiving an email or WhatsApp notification with a single-click approval link.

No more walking forms between floors. No more "I sent it to you last week" disputes.

## E-Signatures & Audit Trails

All approvals are timestamped with the approver's name, role, device, and IP address. This creates a tamper-proof institutional record that satisfies both internal audits and external regulatory requirements.

In one NGO deployment, this single feature reduced audit preparation time from three weeks to two days.

## Change Management Is Non-Negotiable

Technology is 30% of the challenge. People are 70%. A digital workflow system that staff do not trust or understand will be bypassed in favor of WhatsApp forwards and printed forms within a month.

Successful rollouts dedicate as much effort to staff training, feedback sessions, and phased adoption as they do to the software build itself.

Florante includes structured change management and role-specific training in every digitization project we deliver.""",
        "author_name": "Florante Digital Labs",
        "author_role": "Solutions Desk",
        "tags": ["Digital Transformation", "Workflows", "Paperless", "NGO", "Enterprise"],
        "featured_image": "",
        "is_featured": False,
        "is_published": True,
        "published_at": parse_datetime("2026-08-02T09:15:00Z"),
        "views_count": 289,
        "seo_title": "Replacing Paper Workflows with Digital Systems — Florante Insights",
        "seo_description": "Step-by-step guide to digitizing institutional approval flows and paper forms for African NGOs and enterprises.",
    },
    {
        "title": "Building Scalable APIs for M-Pesa Integration in East Africa",
        "slug": "mpesa-api-integration-guide",
        "category": "software-engineering",
        "excerpt": "A technical guide to designing robust M-Pesa Daraja API integrations that handle real-world transaction volumes without failures.",
        "content": """M-Pesa processes millions of transactions daily across East Africa. Building a reliable integration is not simply a matter of following the Daraja API documentation — it requires thoughtful architecture that handles retries, timeouts, duplicate payments, and callback failures gracefully.

## Understanding the Daraja API Architecture

Safaricom's Daraja platform exposes several key APIs:

- **STK Push (Lipa na M-Pesa Online)** — initiates a payment prompt on the customer's phone.
- **C2B (Customer to Business)** — receives payments sent by customers to a paybill or till number.
- **B2C (Business to Customer)** — sends payments from a business to a customer's M-Pesa wallet.
- **Transaction Status** — queries the status of any transaction by its M-Pesa reference code.

Most payment bugs come from treating STK Push callbacks as guaranteed. They are not.

## Handling Callback Failures

When a customer completes an STK Push payment, Safaricom sends a callback to your registered URL. If your server is down, busy, or returns a non-200 HTTP response, the callback is lost. Permanently.

The correct architecture:

1. When an STK Push is initiated, create a **pending transaction record** in your database immediately.
2. Accept the callback and return 200 OK within 2 seconds — any processing beyond this must happen asynchronously.
3. Run a **transaction reconciliation job** every 5 minutes using the Transaction Status API to catch any missed callbacks.

## Idempotency Is Critical

Network issues can cause the same payment to trigger multiple callbacks. Every payment processing endpoint must be idempotent — processing the same M-Pesa reference code twice must produce the same final state, not double the credit.

Use the M-Pesa `TransactionID` as a unique key in your payments table with a database-level unique constraint.

## Testing Without Real Money

Use Safaricom's sandbox environment during development with test credentials. Never test payment flows on production with real customer money — even small amounts cause real accounting discrepancies and customer confusion.

Build a separate `is_sandbox` flag in your payment configuration that routes all transactions to the sandbox environment in development and staging.

Florante has built M-Pesa integrations for universities, SACCOs, and retail platforms across Kenya. Reach out if you need a reliable integration built for your system.""",
        "author_name": "Florante Engineering",
        "author_role": "Backend Systems Team",
        "tags": ["M-Pesa", "API", "Software Engineering", "Fintech", "Kenya"],
        "featured_image": "",
        "is_featured": False,
        "is_published": True,
        "published_at": parse_datetime("2026-07-28T08:00:00Z"),
        "views_count": 671,
        "seo_title": "M-Pesa Daraja API Integration Guide — Florante Insights",
        "seo_description": "Technical guide to building scalable, reliable M-Pesa integrations with proper callback handling, idempotency, and reconciliation.",
    },
    {
        "title": "Why African Universities Are Investing in Student Experience Technology",
        "slug": "university-student-experience-tech",
        "category": "education-technology",
        "excerpt": "From digital accommodation booking to alumni engagement portals — how campus technology is reshaping the African university experience.",
        "content": """African universities are under pressure. Rising student enrolment numbers, shrinking administrative budgets, and increasing student expectations are colliding. The institutions finding a way through this pressure are the ones investing in purpose-built campus technology.

## The Accommodation Crisis

Every major Kenyan university faces the same problem during registration week: thousands of students, too few rooms, manual allocation spreadsheets, and endless queues at the accommodation office. Students wait for days. Staff work through the night. Errors pile up.

Digital accommodation platforms solve this structurally. Students log in, see available rooms in real time, select their preference, pay via M-Pesa, and receive an instant digital gate pass. The queue disappears entirely.

The administrative impact is equally significant. Housing officers shift from data entry to exception handling. Occupancy reporting that once took three days runs automatically overnight.

## Beyond Accommodation — The Connected Campus

Forward-thinking universities are connecting disparate systems into a unified student portal:

- **Fee management** — automated M-Pesa verification removes the need for manual payment clearance.
- **Timetabling** — conflict-free schedule generation reduces lecturer coordination overhead by 60%.
- **Library systems** — digital borrowing and reservation reduces physical desk traffic.
- **Alumni portals** — connecting graduates with career opportunities and donation programs.

Each system individually creates value. Connected together, they create a campus that operates efficiently at scale.

## The ROI Conversation

University administrators often frame technology as a cost. The framing should be inverted. A digital accommodation system that eliminates three weeks of administrative overtime per semester, reduces fee reconciliation errors, and enables self-service for 10,000 students pays for itself in the first year.

The question is not whether African universities can afford campus technology. It is whether they can afford to compete without it.""",
        "author_name": "Florante Solutions Desk",
        "author_role": "Education Technology Practice",
        "tags": ["Education Technology", "University", "Student Experience", "Africa"],
        "featured_image": "",
        "is_featured": False,
        "is_published": True,
        "published_at": parse_datetime("2026-07-20T11:00:00Z"),
        "views_count": 203,
        "seo_title": "Student Experience Technology for African Universities — Florante Insights",
        "seo_description": "How campus technology — from digital accommodation to alumni portals — is reshaping the African university experience.",
    },
]


class Command(BaseCommand):
    help = "Seed article records into the database"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in ARTICLES:
            obj, was_created = Article.objects.update_or_create(
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
                f"\nDone — {created} created, {updated} updated. Total articles: {Article.objects.count()}"
            )
        )
