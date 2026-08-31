from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from apps.labs.models import Hackathon

HACKATHONS = [
    {
        "title": "Florante AI Challenge 2026",
        "slug": "florante-ai-challenge-2026",
        "tagline": "Build AI that works for Africa — not just about Africa.",
        "description": "Africa's most practical AI hackathon. Build machine learning tools, automation pipelines, and intelligent systems that solve real operational problems for African businesses, schools, and governments.",
        "long_description": """The Florante AI Challenge is not about impressive demos — it is about deployable solutions. We are looking for teams that identify a real operational pain point faced by African organizations and build an AI-powered tool that genuinely solves it.

Past winning projects have included an automated M-Pesa reconciliation engine, a Swahili-language document classifier for a county government, and a demand forecasting model for a Nairobi distributor.

**What we are looking for:**
- A clearly defined real-world problem with an identifiable user
- A working AI/ML prototype that addresses that problem
- A viable path to production deployment
- A presentation that demonstrates measurable impact

All skill levels are welcome. Participants receive access to cloud compute credits, Florante API sandbox environments, and mentorship from our engineering and AI team throughout the challenge.""",
        "rules": """1. Teams of 1–4 participants.
2. All code must be written during the hackathon period.
3. Open source libraries and pre-trained models are permitted.
4. Solutions must use at least one AI or machine learning component.
5. Submissions must include a working demo, source code, and a 5-minute presentation video.
6. Judging criteria: Problem clarity (25%), Technical quality (25%), Impact potential (25%), Presentation (25%).
7. Florante reserves the right to disqualify teams that use pre-built solutions or violate fair play rules.""",
        "tech_stack": ["Python", "TensorFlow", "PyTorch", "FastAPI", "React", "PostgreSQL", "OpenAI API", "Hugging Face"],
        "prizes": [
            {"place": "1st Place", "reward": "KES 150,000 + 6-month Florante mentorship program"},
            {"place": "2nd Place", "reward": "KES 75,000 + Florante Cloud Credits"},
            {"place": "3rd Place", "reward": "KES 35,000 + Florante API access"},
            {"place": "Best Student Team", "reward": "KES 25,000 + University Partnership Certificate"},
        ],
        "schedule": [
            {"date": "2026-09-15", "event": "Registration Opens"},
            {"date": "2026-10-01", "event": "Team Formation Deadline"},
            {"date": "2026-10-10", "event": "Kickoff & Problem Briefing (Virtual)"},
            {"date": "2026-10-10", "event": "Hacking Period Begins"},
            {"date": "2026-10-17", "event": "Midpoint Check-in & Mentorship Sessions"},
            {"date": "2026-10-24", "event": "Submissions Close (11:59 PM EAT)"},
            {"date": "2026-10-31", "event": "Finalist Presentations (Nairobi)"},
            {"date": "2026-10-31", "event": "Winners Announced & Awards Ceremony"},
        ],
        "sponsors": ["Florante Tech Limited", "Safaricom Developer Program", "Google for Startups Africa", "AWS Activate"],
        "start_date": parse_datetime("2026-10-10T08:00:00+03:00"),
        "deadline": parse_datetime("2026-10-24T23:59:00+03:00"),
        "status": "upcoming",
        "participants_count": 0,
        "image": "",
        "published": True,
    },
    {
        "title": "Florante Cybersecurity CTF 2026",
        "slug": "florante-ctf-2026",
        "tagline": "Find the flag. Protect Africa's digital infrastructure.",
        "description": "A Capture The Flag competition focused on real-world African digital security challenges. Test your skills across web exploitation, API security, cryptography, and network forensics — in scenarios drawn directly from East African institutional environments.",
        "long_description": """The Florante Cybersecurity CTF challenges participants with scenarios based on the real security vulnerabilities and attack patterns we encounter when auditing African digital infrastructure.

This is not a generic CTF. Challenges are themed around M-Pesa API security, East African regulatory compliance, Django/PostgreSQL vulnerabilities, and mobile application security patterns common in the region.

**Challenge categories:**
- Web Application Security (OWASP Top 10)
- API & Authentication Exploitation
- Database Forensics & SQL Injection
- Cryptography & Token Forgery
- Mobile App Reverse Engineering
- Network Traffic Analysis

All participants receive a full post-CTF writeup with detailed solutions and mitigation guidance — making this as much a learning event as a competition.""",
        "rules": """1. Individual participants only — no teams in the CTF.
2. No sharing of flags or answers with other participants during the competition.
3. No attacking the CTF infrastructure itself.
4. All tools must be disclosed in your writeup submission.
5. Top 10 finishers must submit a technical writeup for each flag captured.
6. Florante staff are not eligible to compete.""",
        "tech_stack": ["Burp Suite", "OWASP ZAP", "Wireshark", "Python", "Metasploit", "Nmap", "SQLMap"],
        "prizes": [
            {"place": "1st Place", "reward": "KES 80,000 + Florante Security Internship Offer"},
            {"place": "2nd Place", "reward": "KES 40,000 + OSCP Exam Voucher"},
            {"place": "3rd Place", "reward": "KES 20,000 + Security Toolkit Bundle"},
            {"place": "Most Creative Exploit", "reward": "KES 10,000 Special Award"},
        ],
        "schedule": [
            {"date": "2026-11-01", "event": "Registration Opens"},
            {"date": "2026-11-14", "event": "Registration Closes"},
            {"date": "2026-11-15", "event": "CTF Platform Goes Live (08:00 AM EAT)"},
            {"date": "2026-11-22", "event": "CTF Closes (06:00 PM EAT)"},
            {"date": "2026-11-25", "event": "Writeup Submission Deadline"},
            {"date": "2026-11-28", "event": "Results & Prize Distribution"},
        ],
        "sponsors": ["Florante Tech Limited", "Safaricom Cyber Security", "KENIC"],
        "start_date": parse_datetime("2026-11-15T08:00:00+03:00"),
        "deadline": parse_datetime("2026-11-22T18:00:00+03:00"),
        "status": "upcoming",
        "participants_count": 0,
        "image": "",
        "published": True,
    },
]


class Command(BaseCommand):
    help = "Seed hackathon records into the database"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for data in HACKATHONS:
            obj, was_created = Hackathon.objects.update_or_create(
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
                f"\nDone — {created} created, {updated} updated. Total hackathons: {Hackathon.objects.count()}"
            )
        )
