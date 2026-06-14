from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import PrivacyPolicy

class Command(BaseCommand):
    help = 'Create initial privacy policy'
    
    def handle(self, *args, **options):
        policy_content = """
PRIVACY POLICY FOR AMAKAZIWATCH

Effective Date: January 1, 2025

1. INFORMATION WE COLLECT
   - Personal information you provide (name, email, phone number)
   - Report details including location and incident descriptions
   - Evidence files you upload (photos, documents)
   - Device information and IP addresses for security

2. HOW WE USE YOUR INFORMATION
   - To process and respond to GBV reports
   - To connect you with support organizations
   - To generate anonymous statistics and heatmaps
   - To improve our services and response times

3. DATA PROTECTION
   - All evidence files are encrypted
   - Personal information is stored securely
   - Reports can be submitted anonymously
   - You can request data deletion at any time

4. INFORMATION SHARING
   - We only share information with verified organizations you consent to
   - Anonymous statistics may be shared with partners
   - We never sell your personal information

5. YOUR RIGHTS
   - Access your data
   - Correct inaccurate information
   - Request deletion of your data
   - Withdraw consent at any time

6. CONTACT US
   - Email: privacy@amakaziwatch.com
   - Phone: 1195 (toll-free)
   - Address: Nairobi, Kenya

7. CHANGES TO THIS POLICY
   - We will notify users of significant changes
   - Continued use constitutes acceptance of changes
"""
        
        PrivacyPolicy.objects.create(
            version="1.0",
            content=policy_content,
            effective_date=timezone.now(),
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('Initial privacy policy created'))
