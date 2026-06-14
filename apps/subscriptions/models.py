from django.db import models
from organisations.models import Organisation


class Plan(models.TextChoices):
    FREE     = "free",     "Free"
    NGO_BASIC = "ngo_basic", "NGO Basic — KES 5,000/month"
    NGO_PRO  = "ngo_pro",  "NGO Pro — KES 10,000/month"
    COUNTY   = "county",   "County Government — KES 15,000/month"


class Subscription(models.Model):
    organisation  = models.OneToOneField(Organisation, on_delete=models.CASCADE, related_name="subscription")
    plan          = models.CharField(max_length=20, choices=Plan.choices, default=Plan.FREE)
    is_active     = models.BooleanField(default=False)
    started_at    = models.DateTimeField(null=True, blank=True)
    expires_at    = models.DateTimeField(null=True, blank=True)
    paystack_ref  = models.CharField(max_length=100, blank=True)
    auto_renew    = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def is_valid(self):
        from django.utils import timezone
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            self.is_active = False
            self.save()
            return False
        return True

    def __str__(self):
        return f"{self.organisation.name} — {self.plan} — {'Active' if self.is_active else 'Inactive'}"


class SubscriptionPayment(models.Model):
    class Status(models.TextChoices):
        PENDING   = "pending",   "Pending"
        COMPLETED = "completed", "Completed"
        FAILED    = "failed",    "Failed"

    subscription  = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="payments")
    amount        = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_ref  = models.CharField(max_length=100, blank=True)
    status        = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at       = models.DateTimeField(null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription.organisation.name} — KES {self.amount} — {self.status}"
