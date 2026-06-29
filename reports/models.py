from django.db import models
from django.conf import settings

class Report(models.Model):
    id = models.BigAutoField(primary_key=True)  # Changed from UUID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    abuse_type = models.CharField(max_length=50)
    relationship = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    is_anonymous = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Report #{self.id} - {self.county}"
