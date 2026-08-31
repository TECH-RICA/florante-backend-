from django.core.management.base import BaseCommand
from apps.cms.models import Testimonial, University, FAQ, TeamMember

TESTIMONIALS = [
    {"quote": "Florante transformed our hostel administration from a week of admission chaos into a smooth 10-minute digital experience for every student.", "author": "Dr. James Mwangi", "role": "Dean of Student Affairs", "company": "East African University Partner", "published": True},
    {"quote": "The Sentinel platform gave our board complete real-time visibility over our security posture. We passed our DPA audit without a single critical finding.", "author": "Sarah Otieno", "role": "Head of IT Infrastructure", "company": "Regional Financial Institution", "published": True},
    {"quote": "Flow Forms cut our procurement approval cycle from 5 days to under 4 hours. Our field teams no longer wait on Nairobi HQ for every purchase order.", "author": "Peter Kamau", "role": "Operations Director", "company": "Pan-African NGO", "published": True},
    {"quote": "Florante Core ERP gave us visibility into our three branches that we simply did not have before. Stock discrepancies dropped by 90% in the first month.", "author": "Grace Njeri", "role": "Managing Director", "company": "Wholesale Distribution SME", "published": True},
    {"quote": "Their team understood our regulatory environment from day one. The compliance dashboard they built is now how we prepare for every CBK inspection.", "author": "Michael Ochieng", "role": "Chief Risk Officer", "company": "Kenya SACCO", "published": True},
]

UNIVERSITIES = [
    {"name": "University of Nairobi", "county": "Nairobi"},
    {"name": "Kenyatta University", "county": "Nairobi"},
    {"name": "Strathmore University", "county": "Nairobi"},
    {"name": "Jomo Kenyatta University of Agriculture & Technology", "county": "Kiambu"},
    {"name": "Moi University", "county": "Uasin Gishu"},
    {"name": "Egerton University", "county": "Nakuru"},
    {"name": "Maseno University", "county": "Kisumu"},
    {"name": "Dedan Kimathi University of Technology", "county": "Nyeri"},
    {"name": "Kirinyaga University", "county": "Kirinyaga"},
    {"name": "Multimedia University of Kenya", "county": "Nairobi"},
]

FAQS = [
    {"question": "How do I request a demo or consultation?", "answer": "Click 'Get in touch' or 'Talk to Florante' on any page, or message us directly on WhatsApp at +254 770 428 297. We typically respond within 2 hours during business hours.", "context": "general", "order": 1, "published": True},
    {"question": "Where is Florante Tech located?", "answer": "We are headquartered in Kirinyaga, Kenya, and serve clients across East Africa. We deliver projects remotely and on-site depending on the engagement.", "context": "general", "order": 2, "published": True},
    {"question": "Do you sign NDAs before discovery sessions?", "answer": "Yes. We are happy to sign a mutual NDA before any technical discovery conversation. Contact us to initiate the process.", "context": "general", "order": 3, "published": True},
    {"question": "What is your typical project delivery timeline?", "answer": "Small projects (e.g. a single module or integration) take 2–4 weeks. Full platform builds typically run 8–16 weeks with phased milestone deliveries.", "context": "general", "order": 4, "published": True},
    {"question": "Do you offer post-launch support and maintenance?", "answer": "Yes. All projects include a 3-month post-launch support window. Long-term maintenance retainers are available for ongoing updates and monitoring.", "context": "general", "order": 5, "published": True},
    {"question": "Can Unicrib integrate with our student information system?", "answer": "Yes. Unicrib exposes a full REST API that can sync bidirectionally with any existing student management or ERP system.", "context": "products", "order": 1, "published": True},
    {"question": "Does your software support M-Pesa payments?", "answer": "Yes. M-Pesa Daraja API integration is a core capability across our products, including real-time STK Push, C2B paybill, and automated reconciliation.", "context": "products", "order": 2, "published": True},
    {"question": "How do you handle our data security and privacy?", "answer": "All data is encrypted in transit (TLS 1.3) and at rest (AES-256). We follow Kenya DPA requirements, implement RBAC, and maintain full audit trails for all data access.", "context": "products", "order": 3, "published": True},
    {"question": "What does a cybersecurity audit involve?", "answer": "Our audit covers OWASP vulnerability scanning, API security review, network exposure mapping, compliance gap analysis, and a prioritized remediation report with fix instructions.", "context": "cybersecurity", "order": 1, "published": True},
    {"question": "How long does a penetration test take?", "answer": "A standard web and API penetration test takes 5–7 business days from scope agreement to delivery of the findings report.", "context": "cybersecurity", "order": 2, "published": True},
]

TEAM = [
    {"name": "Willy Maina", "role": "Lead Systems Architect & Founder", "bio": "Passionate software engineer building resilient cloud platforms, AI automation tools, and secure web architectures for African institutions. 7+ years across fintech, edtech, and enterprise software.", "image": "", "portfolio_url": "", "linkedin": "https://linkedin.com", "github": "https://github.com/willy-maina", "twitter": "", "order": 1, "published": True},
    {"name": "Florante Engineering", "role": "Core Software & AI Desk", "bio": "Cross-functional engineering team specializing in Django microservices, React UI frameworks, data pipeline security, and machine learning model deployment for African operational environments.", "image": "", "portfolio_url": "", "linkedin": "https://linkedin.com", "github": "https://github.com", "twitter": "", "order": 2, "published": True},
    {"name": "Florante Solutions Desk", "role": "Digital Strategy & Security", "bio": "Dedicated team guiding organizational digitization, ISO cybersecurity compliance, Kenya DPA advisory, and enterprise cloud migration programs.", "image": "", "portfolio_url": "", "linkedin": "https://linkedin.com", "github": "https://github.com", "twitter": "", "order": 3, "published": True},
]


class Command(BaseCommand):
    help = "Seed testimonials, universities, FAQs, and team members"

    def handle(self, *args, **options):
        # Testimonials
        Testimonial.objects.all().delete()
        for d in TESTIMONIALS:
            Testimonial.objects.create(**d)
        self.stdout.write(self.style.SUCCESS(f"  Testimonials: {Testimonial.objects.count()} created"))

        # Universities
        for d in UNIVERSITIES:
            University.objects.get_or_create(name=d["name"], defaults={"county": d["county"]})
        self.stdout.write(self.style.SUCCESS(f"  Universities: {University.objects.count()} total"))

        # FAQs
        FAQ.objects.all().delete()
        for d in FAQS:
            FAQ.objects.create(**d)
        self.stdout.write(self.style.SUCCESS(f"  FAQs: {FAQ.objects.count()} created"))

        # Team
        TeamMember.objects.all().delete()
        for d in TEAM:
            TeamMember.objects.create(**d)
        self.stdout.write(self.style.SUCCESS(f"  Team members: {TeamMember.objects.count()} created"))

        self.stdout.write(self.style.SUCCESS("\nAll CMS records seeded successfully."))
