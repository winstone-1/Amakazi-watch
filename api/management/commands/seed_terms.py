from django.core.management.base import BaseCommand
from django.utils import timezone
from api.terms_models import TermsOfService

class Command(BaseCommand):
    help = 'Seed Terms of Service in English and Swahili'

    def handle(self, *args, **options):
        terms_en = """
TERMS OF SERVICE FOR AMAKAZIWATCH

Version: 1.0
Effective Date: January 1, 2025

1. PURPOSE
AmakaziWatch is a reporting and support platform for Gender-Based Violence (GBV) in Kenya. This is NOT an emergency service. For immediate danger, call 1195 or 999.

2. USER RESPONSIBILITIES
- Provide truthful and accurate information
- Do not submit false or malicious reports
- Treat all users with respect
- Do not harass or impersonate others

3. ORGANIZATION RESPONSIBILITIES
- Maintain verified status
- Keep resource inventory updated
- Respond to referrals within 24 hours
- Maintain survivor confidentiality

4. PROHIBITED CONTENT
- False or misleading reports
- Hate speech or incitement to violence
- Sharing explicit images without consent
- Attempting to identify anonymous reporters

5. DATA AND PRIVACY
- Anonymous reports are truly anonymous (no IP logging)
- Your data is encrypted and never sold
- You can export or delete your data at any time

6. LIMITATION OF LIABILITY
- AmakaziWatch connects survivors with organizations but is not responsible for their actions
- We do not guarantee response times from organizations

7. ACCOUNT TERMINATION
- Violations lead to immediate account suspension
- False reports referred to authorities

8. DISPUTE RESOLUTION
- Kenyan law applies
- Exclusive jurisdiction: Nairobi, Kenya courts

9. CONTACT
- Terms questions: legal@amakaziwatch.com
- Emergency: 1195 (toll-free)
"""

        terms_sw = """
MASHARTI YA MATUMIZI YA AMAKAZIWATCH

Toleo: 1.0
Tarehe ya Kuanza: Januari 1, 2025

1. MADHUMUNI
AmakaziWatch ni jukwaa la kuripoti na kusaidia dhidi ya Unyanyasaji wa Kijinsia (GBV) nchini Kenya. HUDUMU HIYO SI YA DHARURA. Kwa hatari ya haraka, piga 1195 au 999.

2. MAJUKUMU YA MTUMIAJI
- Toa taarifa za kweli na sahihi
- Usiwasilishe ripoti za uongo au zenye nia mbaya
- Watende watu wote kwa heshima
- Usiwanyanyase au kuwajifanya watu wengine

3. MAJUKUMU YA SHIRIKA
- Dumisha hali ya uthibitishaji
- Weka orodha ya rasilimali iliyosasishwa
- Jibu marejeleo ndani ya saa 24
- Dumisha usiri wa waathirika

4. MAUDHUI YALIYOPIGWA MARUFUKU
- Ripoti za uongo au zenye kupotosha
- Matamshi ya chuki au uchochezi wa vurugu
- Kushiriki picha zisizo halali bila idhini
- Kujaribu kutambua wanahabari wasiojulikana

5. DATA NA USIRI
- Ripoti zisizojulikana ni za siri kabisa (hakuna kurekodi IP)
- Data yako imesimbwa na haiuuzwi kamwe
- Unaweza kuhamisha au kufuta data yako wakati wowote

6. KIKOMO CHA DHIMANA
- AmakaziWatch inaunganisha waathirika na mashirika lakini haiwajibiki kwa vitendo vyao
- Hatuhakikishi muda wa majibu kutoka kwa mashirika

7. KUSITISHWA KWA AKAUNTI
- Ukiukaji husababisha kusimamishwa kwa akaunti mara moja
- Ripoti za uongo zinaelekezwa kwa mamlaka

8. UTATUZI WA MIZOZO
- Sheria ya Kenya inatumika
- Mamlaka ya pekee: Mahakama za Nairobi, Kenya

9. MAWASILIANO
- Maswali ya masharti: legal@amakaziwatch.com
- Dharura: 1195 (bila malipo)
"""

        TermsOfService.objects.create(
            version="1.0",
            content_en=terms_en,
            content_sw=terms_sw,
            effective_date=timezone.now(),
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('Terms of Service seeded in English and Swahili'))
