from django.db import models
from users.models import User


class Notification(models.Model):
    class Type(models.TextChoices):
        REPORT_SPIKE   = "report_spike",   "Report Spike in County"
        NEW_REFERRAL   = "new_referral",   "New Referral Received"
        CONTENT_APPROVED = "content_approved", "Content Approved"
        SUBSCRIPTION   = "subscription",   "Subscription Update"
        SYSTEM         = "system",         "System Alert"

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type       = models.CharField(max_length=30, choices=Type.choices)
    title      = models.CharField(max_length=200)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} — {self.title}"


class AuditLog(models.Model):
    user       = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action     = models.CharField(max_length=200)
    model_name = models.CharField(max_length=100, blank=True)
    object_id  = models.CharField(max_length=100, blank=True)
    details    = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} — {self.action} — {self.created_at}"
