from django.core.management.base import BaseCommand
from apps.solutions.models import Solution

SOLUTIONS = [
    {
        "title": "AI & Automation",
        "slug": "ai-automation",
        "category": "ai-automation",
        "short_description": "Intelligent machine learning and automation systems designed to streamline workflows and drive predictive decisions.",
        "hero_text": "Automate repetitive tasks, build custom ML models, and gain predictive insights with enterprise AI engineered for African operational environments.",
        "problem": "Organizations lose thousands of hours every month on manual data entry, repetitive document processing, and delayed operational decision making.",
        "approach": "We design and deploy custom AI models, NLP engines, and Robotic Process Automation (RPA) workflows tailored to your specific organizational context.",
        "cta_text": "Talk to our AI team",
        "published": True,
        "capabilities": [
            "Custom ML Model Development",
            "Robotic Process Automation (RPA)",
            "Natural Language Processing & Speech",
            "Predictive Analytics & Forecasting",
        ],
        "use_cases": [
            "Automated Document Processing",
            "Customer Support Chatbots",
            "Risk & Fraud Scoring Models",
            "Operational Demand Forecasting",
        ],
        "benefits": [
            "Reduce operational costs by up to 40%",
            "24/7 automated task execution",
            "Faster data-driven decision making",
            "Scale operations without linear headcount growth",
        ],
        "technologies": ["Python", "PyTorch", "TensorFlow", "FastAPI", "Celery", "OpenAI"],
        "faqs": [
            {"question": "Do we need to provide training data?", "answer": "It depends on the use case. Many automation tasks work well with your existing operational data. We'll assess this in a discovery session."},
            {"question": "How long does a typical AI project take?", "answer": "A focused RPA or ML deployment typically takes 4–8 weeks from discovery to production."},
        ],
        "seo_title": "AI & Automation Solutions — Florante Tech",
        "seo_description": "Enterprise AI, RPA, and machine learning systems built for African organizations. Automate workflows and drive smarter decisions.",
    },
    {
        "title": "Cybersecurity & Protection",
        "slug": "cybersecurity",
        "category": "cybersecurity",
        "short_description": "Comprehensive security assessments, penetration testing, compliance, and threat monitoring for modern enterprises.",
        "hero_text": "Safeguard your critical systems, cloud applications, and sensitive client data from evolving cybersecurity threats.",
        "problem": "Cyber attacks in East Africa are growing rapidly, targeting unprotected web, mobile, and API endpoints without continuous security monitoring.",
        "approach": "Proactive security auditing, penetration testing, automated threat detection, and end-to-end security architecture aligned with ISO 27001 & the Kenya Data Protection Act.",
        "cta_text": "Get a Security Audit",
        "published": True,
        "capabilities": [
            "Penetration Testing & Vulnerability Assessment",
            "API & Web Application Security",
            "Data Protection & ISO Compliance Audits",
            "Incident Response & Forensics",
        ],
        "use_cases": [
            "Banking & Fintech Security Audits",
            "Healthcare Data Privacy Assurance",
            "Cloud Infrastructure Hardening",
            "Regulatory Compliance Preparation",
        ],
        "benefits": [
            "Mitigate data breach and reputational risks",
            "Build institutional trust with secure systems",
            "Full compliance with Kenyan & African data privacy laws",
            "Real-time threat visibility",
        ],
        "technologies": ["OWASP", "Burp Suite", "WAF", "Docker", "Vault", "SIEM"],
        "faqs": [
            {"question": "How often should a security audit be done?", "answer": "We recommend quarterly vulnerability assessments and a full penetration test annually, or after any major system change."},
            {"question": "Do you help with Kenya Data Protection Act compliance?", "answer": "Yes, we provide full DPA gap analysis, remediation roadmaps, and documentation for regulatory submission."},
        ],
        "seo_title": "Cybersecurity Solutions — Florante Tech",
        "seo_description": "Penetration testing, compliance audits, and threat monitoring for African enterprises. Protect your systems with Florante.",
    },
    {
        "title": "Software Engineering",
        "slug": "software-engineering",
        "category": "software-engineering",
        "short_description": "High-performance web applications, mobile platforms, and enterprise software built with modern architectures.",
        "hero_text": "Scalable web apps, mobile systems, and microservice APIs engineered for reliable performance and business growth.",
        "problem": "Generic off-the-shelf software rarely fits complex organizational workflows, leading to clunky workarounds, data silos, and poor user satisfaction.",
        "approach": "We build custom, maintainable web and mobile applications using modern clean architecture, scalable databases, and automated testing.",
        "cta_text": "Discuss Your Software Project",
        "published": True,
        "capabilities": [
            "Custom Web Application Development",
            "Cross-Platform Mobile Apps (iOS/Android)",
            "REST & GraphQL API Architecture",
            "Database Design & Optimization",
        ],
        "use_cases": [
            "Enterprise ERP & Core Portals",
            "Customer Facing Portals & Marketplaces",
            "Mobile Money & Payment Portals",
            "Field Agent Mobile Tools",
        ],
        "benefits": [
            "100% tailored to your business rules",
            "High performance under heavy load",
            "Full code ownership and zero lock-in",
            "Seamless third-party API integration",
        ],
        "technologies": ["React", "TypeScript", "Python / Django", "PostgreSQL", "Tailwind CSS", "Redis"],
        "faqs": [
            {"question": "Do you provide post-launch support?", "answer": "Yes, all our software projects include a 3-month support window and optional long-term maintenance contracts."},
            {"question": "What is your typical project timeline?", "answer": "Small projects take 4–6 weeks. Enterprise platforms typically run 3–6 months with phased delivery milestones."},
        ],
        "seo_title": "Software Engineering Solutions — Florante Tech",
        "seo_description": "Custom web apps, mobile platforms, and enterprise software engineered for African businesses by Florante Tech.",
    },
    {
        "title": "Digital Transformation",
        "slug": "digital-transformation",
        "category": "digital-transformation",
        "short_description": "Legacy system modernization, cloud migration, and workflow digitization for African institutions.",
        "hero_text": "Transition from paper, spreadsheets, and legacy systems to modern cloud-first operations.",
        "problem": "Legacy paper processes and disconnected spreadsheets slow organizational growth, create compliance risks, and cause data loss.",
        "approach": "We audit existing workflows and build connected digital portals that digitize paper processes end-to-end with real-time tracking.",
        "cta_text": "Start Digital Transformation",
        "published": True,
        "capabilities": [
            "End-to-End Workflow Digitization",
            "Cloud Infrastructure Migration",
            "Legacy System API Wrapping",
            "Digital Customer & Staff Onboarding",
        ],
        "use_cases": [
            "Paperless NGO & Enterprise Workflows",
            "University Digital Student Records",
            "SME Operations Automation",
            "Multi-Branch Reporting Systems",
        ],
        "benefits": [
            "Eliminate paper bottlenecks and manual errors",
            "Centralized real-time operational data",
            "Empower remote & multi-branch staff",
            "Reduce operational cycle times by 60%",
        ],
        "technologies": ["Cloud Architecture", "Docker", "REST APIs", "React", "PostgreSQL"],
        "faqs": [
            {"question": "How do you handle staff resistance to change?", "answer": "We include structured change management and hands-on training in every digital transformation project."},
            {"question": "Can we migrate our existing data?", "answer": "Yes, data migration is a core part of every transformation engagement — we handle extraction, cleaning, and validation."},
        ],
        "seo_title": "Digital Transformation Solutions — Florante Tech",
        "seo_description": "Legacy modernization, cloud migration, and paperless workflow digitization for African organizations. Built by Florante Tech.",
    },
    {
        "title": "Data & Intelligence",
        "slug": "data-intelligence",
        "category": "data-intelligence",
        "short_description": "Data pipelines, warehousing, custom dashboards, and business intelligence solutions.",
        "hero_text": "Turn scattered operational data into clear, actionable business dashboards and predictive insights.",
        "problem": "Operational data is trapped across separate software systems and spreadsheets, making real-time reporting and decision-making slow and difficult.",
        "approach": "We consolidate data sources into unified data warehouses and build interactive real-time executive dashboards.",
        "cta_text": "Build Your Data Dashboard",
        "published": True,
        "capabilities": [
            "Data Pipeline (ETL/ELT) Engineering",
            "Centralized Data Warehousing",
            "Interactive Executive Dashboards",
            "Operational & Financial Reporting",
        ],
        "use_cases": [
            "Executive Performance Dashboards",
            "Multi-Location Sales Analytics",
            "Financial Portfolio Reporting",
            "Supply Chain Data Tracking",
        ],
        "benefits": [
            "Single source of truth for leadership",
            "Automated daily/weekly reporting",
            "Faster response to market changes",
            "Uncover hidden revenue opportunities",
        ],
        "technologies": ["Python", "PostgreSQL", "Metabase", "Pandas", "Celery"],
        "faqs": [
            {"question": "Can you connect to our existing software?", "answer": "Yes, we build data connectors for ERP systems, CRMs, payment gateways, and any system with an API or database."},
            {"question": "How long before we see our first dashboard?", "answer": "A first working dashboard prototype is typically ready within 2–3 weeks of data source access."},
        ],
        "seo_title": "Data & Intelligence Solutions — Florante Tech",
        "seo_description": "Data pipelines, business intelligence dashboards, and analytics systems for African enterprises. Powered by Florante Tech.",
    },
]


class Command(BaseCommand):
    help = "Seed solution records into the database"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in SOLUTIONS:
            obj, was_created = Solution.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {obj.title}"))
            else:
                updated += 1
                self.stdout.write(f"  Updated: {obj.title}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created} created, {updated} updated. Total solutions: {Solution.objects.count()}"
            )
        )
