from django.db import models
from django.conf import settings
from django.utils import timezone

class TermsOfService(models.Model):
    version = models.CharField(max_length=20)
    content_en = models.TextField()
    content_sw = models.TextField()
    effective_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-effective_date']
    
    def get_content(self, language='en'):
        return self.content_sw if language == 'sw' else self.content_en

class UserTermsAcceptance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    terms_version = models.ForeignKey(TermsOfService, on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    language = models.CharField(max_length=10, default='en')
