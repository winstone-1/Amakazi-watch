from django.core.management.base import BaseCommand
from organisations.models import Organisation
from reports.models import IncidentReport
from content.models import EducationContent, Quiz


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Clear existing data
        Organisation.objects.all().delete()
        IncidentReport.objects.all().delete()
        EducationContent.objects.all().delete()
        Quiz.objects.all().delete()

        # Organisations
        org1 = Organisation.objects.create(
            name='GVRC Nairobi',
            description='Gender Violence Recovery Centre at Nairobi Hospital. Provides medical, psychological and legal support to survivors.',
            services='counselling,legal aid,medical support,safe shelter',
            county='Nairobi',
            sub_county='Upperhill',
            phone='0800720500',
            email='info@gvrc.or.ke',
            website='https://gvrc.or.ke',
            latitude=-1.2921,
            longitude=36.8219,
            verified=True,
        )

        org2 = Organisation.objects.create(
            name='FIDA Kenya',
            description='Federation of Women Lawyers in Kenya. Provides free legal aid to women and children survivors of GBV.',
            services='legal aid,court representation,legal education,psychosocial support',
            county='Nairobi',
            sub_county='Kilimani',
            phone='0202721784',
            email='fida@fidakenya.org',
            website='https://fidakenya.org',
            latitude=-1.2864,
            longitude=36.7819,
            verified=True,
        )

        org3 = Organisation.objects.create(
            name='Wangu Kanja Foundation',
            description='Community-based organisation supporting GBV survivors in Meru County through counselling and livelihood programs.',
            services='counselling,livelihood support,community awareness,safe house referrals',
            county='Meru',
            sub_county='Imenti North',
            phone='0722000111',
            email='info@wangukanja.org',
            website='https://wangukanja.org',
            latitude=0.0467,
            longitude=37.6491,
            verified=True,
        )

        self.stdout.write('  Created 3 organisations')

        # Incident Reports
        reports_data = [
            {
                'abuse_type': 'physical',
                'relationship': 'family',
                'county': 'Nairobi',
                'sub_county': 'Kasarani',
                'description': 'Repeated physical assault by family member over the past three months.',
                'sms_ref_code': 'NBI00001',
                'urgency_score': 4,
            },
            {
                'abuse_type': 'emotional',
                'relationship': 'colleague',
                'county': 'Mombasa',
                'sub_county': 'Nyali',
                'description': 'Ongoing harassment and intimidation at workplace.',
                'sms_ref_code': 'MBA00002',
                'urgency_score': 2,
            },
            {
                'abuse_type': 'financial',
                'relationship': 'family',
                'county': 'Kisumu',
                'sub_county': 'Kisumu Central',
                'description': 'Spouse controlling all household finances and withholding money for basic needs.',
                'sms_ref_code': 'KSM00003',
                'urgency_score': 3,
            },
            {
                'abuse_type': 'digital',
                'relationship': 'other',
                'county': 'Nakuru',
                'sub_county': 'Nakuru East',
                'description': 'Threatening messages and sharing of private photos without consent.',
                'sms_ref_code': 'NKR00004',
                'urgency_score': 3,
                'flagged_for_review': True,
            },
            {
                'abuse_type': 'physical',
                'relationship': 'self',
                'county': 'Nairobi',
                'sub_county': 'Mathare',
                'description': 'Assault by neighbour. Children also present during incident.',
                'sms_ref_code': 'NBI00005',
                'urgency_score': 5,
                'flagged_for_review': True,
            },
        ]

        for data in reports_data:
            IncidentReport.objects.create(**data)

        self.stdout.write('  Created 5 incident reports')

        # Education Content
        EducationContent.objects.create(
            title='Recognising the Early Signs of Abuse',
            body='Abuse rarely starts with physical violence. Learn how to identify early warning signs including control, isolation, and emotional manipulation.',
            format='article',
            topic='recognise',
            organisation=org1,
            approved=True,
        )

        EducationContent.objects.create(
            title='Your Legal Rights Under the PADV Act 2015',
            body='The Protection Against Domestic Violence Act gives survivors clear legal protections. This guide explains what you are entitled to and how to access justice.',
            format='guide',
            topic='legal',
            organisation=org2,
            approved=True,
        )

        EducationContent.objects.create(
            title='How to Support a Survivor',
            body='If someone you know is experiencing GBV, your response matters. This article explains how to listen, what to say, and how to help safely.',
            format='article',
            topic='support',
            organisation=org3,
            approved=True,
        )

        self.stdout.write('  Created 3 education content items')

        # Quizzes
        Quiz.objects.create(
            title='Do You Recognise Abuse?',
            topic='recognise',
            organisation=org1,
            approved=True,
            questions=[
                {
                    'question': 'Which of these is a form of abuse?',
                    'options': [
                        'A partner checking your phone without permission',
                        'A partner asking where you are going',
                        'A partner cooking dinner for you',
                        'A partner buying you gifts'
                    ],
                    'correct_index': 0
                },
                {
                    'question': 'Financial abuse includes:',
                    'options': [
                        'Helping manage household expenses',
                        'Controlling all money and preventing you from working',
                        'Paying bills on time',
                        'Opening a joint bank account'
                    ],
                    'correct_index': 1
                },
                {
                    'question': 'Isolating a partner from friends and family is:',
                    'options': [
                        'Normal in a relationship',
                        'A sign of love',
                        'A form of emotional abuse',
                        'Only a problem if it happens often'
                    ],
                    'correct_index': 2
                },
            ]
        )

        self.stdout.write('  Created 1 quiz')
        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
