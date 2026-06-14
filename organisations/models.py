from django.db import models

class Organisation(models.Model):
    class OrgType(models.TextChoices):
        NGO            = "ngo",            "NGO"
        COUNTY_GOVT    = "county_govt",    "County Government"
        LEGAL_AID      = "legal_aid",      "Legal Aid Clinic"
        HEALTH         = "health",         "Health Facility"
        COUNSELLING    = "counselling",    "Counselling Centre"
        OTHER          = "other",          "Other"

    name         = models.CharField(max_length=200)
    org_type     = models.CharField(max_length=20, choices=OrgType.choices, default=OrgType.NGO)
    description  = models.TextField()
    services     = models.TextField(help_text="Comma-separated list of services")
    county       = models.CharField(max_length=100)
    sub_county   = models.CharField(max_length=100, blank=True)
    phone        = models.CharField(max_length=20, blank=True)
    email        = models.EmailField(blank=True)
    website      = models.URLField(blank=True)
    latitude     = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude    = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    document_url = models.URLField(blank=True)
    verified     = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_org_type_display()})"


class Donation(models.Model):
    class Status(models.TextChoices):
        PENDING   = "pending",   "Pending"
        COMPLETED = "completed", "Completed"
        FAILED    = "failed",    "Failed"

    organisation      = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="donations")
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    phone             = models.CharField(max_length=100)
    mpesa_checkout_id = models.CharField(max_length=100, blank=True)
    mpesa_receipt     = models.CharField(max_length=100, blank=True)
    status            = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organisation} - KES {self.amount} - {self.status}"


class Referral(models.Model):
    class Status(models.TextChoices):
        PENDING   = "pending",   "Pending"
        ACCEPTED  = "accepted",  "Accepted"
        REJECTED  = "rejected",  "Rejected"
        COMPLETED = "completed", "Completed"

    from_org   = models.ForeignKey("organisations.Organisation", on_delete=models.CASCADE, related_name="referrals_sent")
    to_org     = models.ForeignKey("organisations.Organisation", on_delete=models.CASCADE, related_name="referrals_received")
    ref_code   = models.CharField(max_length=12)
    reason     = models.TextField()
    status     = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_org.name} to {self.to_org.name} [{self.ref_code}] — {self.status}"


class OrganisationReview(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="reviews")
    rating       = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review       = models.TextField()
    helpful      = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organisation.name} — {self.rating}/5"
