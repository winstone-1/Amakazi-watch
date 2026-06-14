from django.db import models
from django.conf import settings

class SafetyTimer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duration_minutes = models.IntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('checked_in', 'Checked In'),
        ('escalated', 'Escalated'),
        ('cancelled', 'Cancelled')
    ])
    location_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    location_lng = models.DecimalField(max_digits=10, decimal_places=7, null=True)

class SafeWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code_word = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RiskAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    risk_level = models.CharField(max_length=20)
    safety_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    answers_json = models.JSONField()

class EscapePlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    documents_checklist = models.JSONField()
    transportation_plan = models.TextField()
    safe_locations = models.JSONField()
    emergency_contacts = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)