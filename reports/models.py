from django.db import models
from django.conf import settings


class IncidentReport(models.Model):
    id = models.AutoField(primary_key=True)  # Changed from UUID to AutoField
    ABUSE_TYPES = [
        ('physical', 'Physical Abuse'),
        ('sexual', 'Sexual Abuse'),
        ('emotional', 'Emotional Abuse'),
        ('economic', 'Economic Abuse'),
        ('digital', 'Digital Abuse'),
        ('other', 'Other'),
    ]

    RELATIONSHIP_CHOICES = [
        ('self', 'Self'),
        ('family', 'Family Member'),
        ('partner', 'Partner/Spouse'),
        ('friend', 'Friend'),
        ('colleague', 'Colleague'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    abuse_type = models.CharField(max_length=20, choices=ABUSE_TYPES)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    is_anonymous = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_abuse_type_display()} - {self.county} ({self.created_at.date()})"


class Report(models.Model):
    id = models.AutoField(primary_key=True)  # Changed from UUID to AutoField
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    abuse_type = models.CharField(max_length=50)
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