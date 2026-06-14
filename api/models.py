from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class PrivacyPolicy(models.Model):
    version = models.CharField(max_length=20)
    content = models.TextField()
    effective_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"Privacy Policy v{self.version} - {self.effective_date.date()}"

class UserConsent(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    policy_version = models.ForeignKey(PrivacyPolicy, on_delete=models.CASCADE)
    consent_given = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'policy_version']
