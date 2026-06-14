from django.core.management.base import BaseCommand
from organisations.models import Organisation
from reports.models import IncidentReport
from content.models import EducationContent, Quiz


class Command(BaseCommand):
    help = "Seed the database with real Kenyan GBV organisations and sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        Organisation.objects.all().delete()
        IncidentReport.objects.all().delete()
        EducationContent.objects.all().delete()
        Quiz.objects.all().delete()

        # Real Kenyan Organisations
        org1 = Organisation.objects.create(
            name="GVRC — Gender Violence Recovery Centre",
            org_type="health",
            description="Located at Nairobi Hospital, GVRC provides integrated medical, psychological, and legal support to survivors of gender-based violence.",
            services="medical support,counselling,legal aid,safe shelter referrals,psychosocial support",
            county="Nairobi",
            sub_county="Upperhill",
            phone="0800720500",
            email="info@gvrc.or.ke",
            website="https://gvrc.or.ke",
            latitude=-1.2995,
            longitude=36.8073,
            verified=True,
        )

        org2 = Organisation.objects.create(
            name="FIDA Kenya — Federation of Women Lawyers",
            org_type="legal_aid",
            description="FIDA Kenya provides free legal aid, court representation and legal education to women and children survivors of GBV across Kenya.",
            services="legal aid,court representation,legal education,psychosocial support,paralegal services",
            county="Nairobi",
            sub_county="Kilimani",
            phone="0202721784",
            email="fida@fidakenya.org",
            website="https://fidakenya.org",
            latitude=-1.2864,
            longitude=36.7819,
            verified=True,
        )

        org3 = Organisation.objects.create(
            name="Wangu Kanja Foundation",
            org_type="ngo",
            description="A survivor-led organisation based in Meru County offering counselling, livelihood programs and community GBV awareness campaigns.",
            services="counselling,livelihood support,community awareness,safe house referrals,survivor support groups",
            county="Meru",
            sub_county="Imenti North",
            phone="0722000111",
            email="info@wangukanja.org",
            website="https://wangukanja.org",
            latitude=0.0467,
            longitude=37.6491,
            verified=True,
        )

        org4 = Organisation.objects.create(
            name="COVAW — Coalition on Violence Against Women",
            org_type="ngo",
            description="COVAW works to end violence against women and girls through advocacy, legal aid, and community empowerment programs across Kenya.",
            services="legal aid,advocacy,community empowerment,safe house referrals,crisis support",
            county="Nairobi",
            sub_county="Westlands",
            phone="0202678991",
            email="info@covaw.or.ke",
            website="https://covaw.or.ke",
            latitude=-1.2673,
            longitude=36.8063,
            verified=True,
        )

        org5 = Organisation.objects.create(
            name="Nairobi County Gender Department",
            org_type="county_govt",
            description="The Nairobi County Government Gender and Social Services department coordinates GBV response, safe house referrals and survivor support within Nairobi County.",
            services="GBV coordination,safe house referrals,county policy,survivor support,inter-agency referrals",
            county="Nairobi",
            sub_county="CBD",
            phone="0202228888",
            email="gender@nairobi.go.ke",
            website="https://nairobi.go.ke",
            latitude=-1.2832,
            longitude=36.8172,
            verified=True,
        )

        org6 = Organisation.objects.create(
            name="KMET — Kisumu Medical and Education Trust",
            org_type="health",
            description="KMET provides reproductive health, GBV response and psychosocial support services across Kisumu and Nyanza region.",
            services="medical support,psychosocial support,community health,GBV response,reproductive health",
            county="Kisumu",
            sub_county="Kisumu Central",
            phone="0572021333",
            email="info@kmet.co.ke",
            website="https://kmet.co.ke",
            latitude=-0.1022,
            longitude=34.7617,
            verified=True,
        )

        self.stdout.write("  Created 6 verified organisations")

        # Incident Reports
        reports_data = [
            {
                "abuse_type": "physical",
                "relationship": "family",
                "county": "Nairobi",
                "sub_county": "Kasarani",
                "description": "Repeated physical assault by family member over the past three months.",
                "sms_ref_code": "NBI00001",
                "urgency_score": 4,
                "flagged_for_review": True,
            },
            {
                "abuse_type": "emotional",
                "relationship": "colleague",
                "county": "Mombasa",
                "sub_county": "Nyali",
                "description": "Ongoing harassment and intimidation at workplace.",
                "sms_ref_code": "MBA00002",
                "urgency_score": 2,
            },
            {
                "abuse_type": "financial",
                "relationship": "family",
                "county": "Kisumu",
                "sub_county": "Kisumu Central",
                "description": "Spouse controlling all household finances and withholding money for basic needs.",
                "sms_ref_code": "KSM00003",
                "urgency_score": 3,
            },
            {
                "abuse_type": "digital",
                "relationship": "other",
                "county": "Nakuru",
                "sub_county": "Nakuru East",
                "description": "Threatening messages and sharing of private photos without consent.",
                "sms_ref_code": "NKR00004",
                "urgency_score": 3,
                "flagged_for_review": True,
            },
            {
                "abuse_type": "physical",
                "relationship": "self",
                "county": "Nairobi",
                "sub_county": "Mathare",
                "description": "Assault by neighbour. Children also present during incident.",
                "sms_ref_code": "NBI00005",
                "urgency_score": 5,
                "flagged_for_review": True,
            },
            {
                "abuse_type": "sexual",
                "relationship": "other",
                "county": "Meru",
                "sub_county": "Imenti South",
                "description": "Incident reported by community member on behalf of survivor.",
                "sms_ref_code": "MRU00006",
                "urgency_score": 5,
                "flagged_for_review": True,
            },
            {
                "abuse_type": "emotional",
                "relationship": "family",
                "county": "Nairobi",
                "sub_county": "Embakasi",
                "description": "Constant verbal abuse and isolation from friends and family.",
                "sms_ref_code": "NBI00007",
                "urgency_score": 2,
            },
            {
                "abuse_type": "financial",
                "relationship": "family",
                "county": "Kisumu",
                "sub_county": "Nyando",
                "description": "Forced to hand over salary every month.",
                "sms_ref_code": "KSM00008",
                "urgency_score": 3,
            },
        ]

        for data in reports_data:
            IncidentReport.objects.create(**data)

        self.stdout.write("  Created 8 incident reports")

        # Education Content
        EducationContent.objects.create(
            title="Recognising the Early Signs of Abuse",
            body="Abuse rarely starts with physical violence. Learn how to identify early warning signs including control, isolation, and emotional manipulation. Financial control, monitoring your movements, and cutting you off from family are all forms of abuse.",
            format="article",
            topic="recognise",
            organisation=org1,
            approved=True,
        )

        EducationContent.objects.create(
            title="Your Legal Rights Under the PADV Act 2015",
            body="The Protection Against Domestic Violence Act 2015 gives survivors clear legal protections in Kenya. You have the right to a protection order, occupation order, and tenancy order. This guide explains what you are entitled to and how to access justice through the courts.",
            format="guide",
            topic="legal",
            organisation=org2,
            approved=True,
        )

        EducationContent.objects.create(
            title="How to Support a Survivor",
            body="If someone you know is experiencing GBV, your response matters deeply. Listen without judgment, believe them, and help them access support. Never pressure them to leave immediately — safety planning takes time. This article explains how to help safely and effectively.",
            format="article",
            topic="support",
            organisation=org3,
            approved=True,
        )

        EducationContent.objects.create(
            title="Understanding Financial Abuse",
            body="Financial abuse is one of the most common but least recognised forms of GBV. It includes controlling all household money, preventing a partner from working, taking their earnings by force, and destroying their credit. It affects both women and men.",
            format="article",
            topic="recognise",
            organisation=org4,
            approved=True,
        )

        EducationContent.objects.create(
            title="Building a Safety Plan",
            body="A safety plan is a personalised guide that helps you prepare for dangerous situations. It includes identifying safe places to go, people to call, important documents to keep accessible, and how to leave safely. COVAW can help you build one.",
            format="guide",
            topic="support",
            organisation=org4,
            approved=True,
        )

        self.stdout.write("  Created 5 education content items")

        # Quizzes
        Quiz.objects.create(
            title="Do You Recognise Abuse?",
            topic="recognise",
            organisation=org1,
            approved=True,
            questions=[
                {
                    "question": "Which of these is a form of abuse?",
                    "options": [
                        "A partner checking your phone without permission",
                        "A partner asking where you are going",
                        "A partner cooking dinner for you",
                        "A partner buying you gifts"
                    ],
                    "correct_index": 0
                },
                {
                    "question": "Financial abuse includes:",
                    "options": [
                        "Helping manage household expenses together",
                        "Controlling all money and preventing you from working",
                        "Opening a joint bank account",
                        "Paying bills on time"
                    ],
                    "correct_index": 1
                },
                {
                    "question": "Isolating a partner from friends and family is:",
                    "options": [
                        "Normal in a relationship",
                        "A sign of love and protectiveness",
                        "A form of emotional abuse",
                        "Only a problem if it happens every day"
                    ],
                    "correct_index": 2
                },
                {
                    "question": "Which organisation provides free legal aid to GBV survivors in Kenya?",
                    "options": [
                        "Kenya Revenue Authority",
                        "FIDA Kenya",
                        "Kenya Power",
                        "Safaricom"
                    ],
                    "correct_index": 1
                },
                {
                    "question": "The national GBV hotline number in Kenya is:",
                    "options": [
                        "999",
                        "116",
                        "1195",
                        "0800"
                    ],
                    "correct_index": 2
                },
            ]
        )

        Quiz.objects.create(
            title="Know Your Legal Rights",
            topic="legal",
            organisation=org2,
            approved=True,
            questions=[
                {
                    "question": "The Protection Against Domestic Violence Act was passed in Kenya in:",
                    "options": ["2010", "2015", "2018", "2020"],
                    "correct_index": 1
                },
                {
                    "question": "A protection order can be issued by:",
                    "options": [
                        "Your employer",
                        "A court of law",
                        "A community elder",
                        "A church leader"
                    ],
                    "correct_index": 1
                },
                {
                    "question": "FIDA Kenya provides legal services:",
                    "options": [
                        "Only to women with money",
                        "Only in Nairobi",
                        "Free of charge to survivors",
                        "Only to married women"
                    ],
                    "correct_index": 2
                },
            ]
        )

        self.stdout.write("  Created 2 quizzes")
        self.stdout.write(self.style.SUCCESS("Seeding complete. Database ready for presentation."))
