from django.db import models
from organisations.models import Organisation

class AwarenessCampaign(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    channels = models.JSONField(default=list)
    target_counties = models.JSONField(default=list)
    scheduled_for = models.DateTimeField()
    sent_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('failed', 'Failed')
    ])
    delivery_stats = models.JSONField(default=dict)