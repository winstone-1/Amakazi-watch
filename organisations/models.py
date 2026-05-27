from django.db import models

class Organisation(models.Model):
    name         = models.CharField(max_length=200)
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
        return self.name


class Donation(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED    = 'failed',    'Failed'

    organisation      = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='donations')
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    phone             = models.CharField(max_length=15)
    mpesa_checkout_id = models.CharField(max_length=100, blank=True)
    mpesa_receipt     = models.CharField(max_length=100, blank=True)
    status            = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organisation} — KES {self.amount} — {self.status}"
