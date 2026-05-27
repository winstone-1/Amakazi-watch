from django.db import models
import uuid

class IncidentReport(models.Model):
    class AbuseType(models.TextChoices):
        PHYSICAL  = 'physical',  'Physical'
        EMOTIONAL = 'emotional', 'Emotional'
        FINANCIAL = 'financial', 'Financial'
        SEXUAL    = 'sexual',    'Sexual'
        DIGITAL   = 'digital',   'Digital'

    class Relationship(models.TextChoices):
        SELF      = 'self',      'Myself'
        FAMILY    = 'family',    'Family Member'
        NEIGHBOUR = 'neighbour', 'Neighbour'
        COLLEAGUE = 'colleague', 'Colleague'
        OTHER     = 'other',     'Other'

    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    abuse_type         = models.CharField(max_length=20, choices=AbuseType.choices)
    relationship       = models.CharField(max_length=20, choices=Relationship.choices)
    county             = models.CharField(max_length=100)
    sub_county         = models.CharField(max_length=100, blank=True)
    description        = models.TextField(blank=True)
    evidence_url       = models.URLField(blank=True)
    sms_ref_code       = models.CharField(max_length=12, blank=True)
    urgency_score      = models.IntegerField(null=True, blank=True)
    ai_classification  = models.CharField(max_length=50, blank=True)
    flagged_for_review = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.abuse_type} — {self.county} — {self.sms_ref_code}"
