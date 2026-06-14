from django.db import models
from users.models import User
import secrets


class APIKey(models.Model):
    class Tier(models.TextChoices):
        FREE       = "free",       "Free — 100 calls/month"
        RESEARCHER = "researcher", "Researcher — 1,000 calls/month — KES 2,000"
        ENTERPRISE = "enterprise", "Enterprise — Unlimited — KES 10,000"

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    name       = models.CharField(max_length=100)
    key        = models.CharField(max_length=64, unique=True)
    tier       = models.CharField(max_length=20, choices=Tier.choices, default=Tier.FREE)
    is_active  = models.BooleanField(default=True)
    calls_made = models.IntegerField(default=0)
    call_limit = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)

    def is_within_limit(self):
        if self.tier == self.Tier.ENTERPRISE:
            return True
        return self.calls_made < self.call_limit

    def increment(self):
        self.calls_made += 1
        self.save()

    def __str__(self):
        return f"{self.user.username} — {self.name} [{self.tier}]"
