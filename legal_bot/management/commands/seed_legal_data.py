from django.core.management.base import BaseCommand
from legal_bot.models import KenyanLawReference

class Command(BaseCommand):
    help = 'Seed legal data for Legal Bot'

    def handle(self, *args, **options):
        laws = [
            {
                "law_name": "Protection Against Domestic Violence Act, 2015",
                "section": "Section 3",
                "summary": "Defines domestic violence and provides protection orders. The court can issue protection orders to prevent further violence.",
                "keywords": ["domestic", "violence", "protection order", "abuse"],
                "full_text_url": "https://www.kenyalaw.org/lex/actview.xql?actid=No.%202%20of%202015"
            },
            {
                "law_name": "Sexual Offences Act, 2006",
                "section": "Section 3",
                "summary": "Defines rape and sexual assault with penalties including life imprisonment.",
                "keywords": ["rape", "sexual assault", "consent", "penalty"],
                "full_text_url": "https://www.kenyalaw.org/lex/actview.xql?actid=No.%203%20of%202006"
            },
            {
                "law_name": "Constitution of Kenya, 2010",
                "section": "Article 27",
                "summary": "Everyone has the right to equal protection and benefit of the law. Discrimination is prohibited.",
                "keywords": ["equality", "rights", "discrimination", "constitution"],
                "full_text_url": "https://www.kenyalaw.org/lex/actview.xql?actid=Const2010"
            },
            {
                "law_name": "Constitution of Kenya, 2010",
                "section": "Article 29",
                "summary": "Every person has the right to freedom and security of the person including freedom from violence.",
                "keywords": ["security", "freedom", "violence", "safety"],
                "full_text_url": "https://www.kenyalaw.org/lex/actview.xql?actid=Const2010"
            },
            {
                "law_name": "Employment Act, 2007",
                "section": "Section 5",
                "summary": "Prohibits discrimination in employment. Employers must not discriminate based on gender or other protected characteristics.",
                "keywords": ["employment", "discrimination", "workplace", "jobs"],
                "full_text_url": "https://www.kenyalaw.org/lex/actview.xql?actid=No.%2011%20of%202007"
            }
        ]

        for law in laws:
            obj, created = KenyanLawReference.objects.get_or_create(
                law_name=law["law_name"],
                section=law["section"],
                defaults=law
            )
            if created:
                self.stdout.write(f"✅ Added: {law['law_name']} - {law['section']}")
            else:
                self.stdout.write(f"⏭️ Skipped: {law['law_name']} already exists")

        self.stdout.write(self.style.SUCCESS("✅ Legal data seeding complete!"))
