from django.db import models

class AnonymousTip(models.Model):
    tip_text = models.TextField()
    incident_county = models.CharField(max_length=50)
    incident_date = models.DateTimeField()
    reporter_relationship = models.CharField(max_length=50, choices=[
        ('neighbor', 'Neighbor'),
        ('colleague', 'Colleague'),
        ('family', 'Family Member'),
        ('professional', 'Professional'),
        ('anonymous', 'Anonymous')
    ])
    is_urgent = models.BooleanField(default=False)
    referred_to_org = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)