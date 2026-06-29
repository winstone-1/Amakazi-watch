from django.db import models
from django.conf import settings
import uuid

class APIKey(models.Model):
    TIER_CHOICES = [
        ('free', 'Free'),
        ('researcher', 'Researcher'),
        ('enterprise', 'Enterprise'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='free')
    requests_this_month = models.IntegerField(default=0)
    monthly_limit = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tier}"

class APIUsageLog(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=200)
    requests_count = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.api_key.user.username} - {self.endpoint}"
