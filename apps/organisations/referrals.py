from django.db import models
from organisations.models import Organisation


class Referral(models.Model):
    class Status(models.TextChoices):
        PENDING   = "pending",   "Pending"
        ACCEPTED  = "accepted",  "Accepted"
        REJECTED  = "rejected",  "Rejected"
        COMPLETED = "completed", "Completed"

    from_org    = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="referrals_sent")
    to_org      = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="referrals_received")
    ref_code    = models.CharField(max_length=12)
    reason      = models.TextField()
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_org.name} → {self.to_org.name} [{self.ref_code}] — {self.status}"
