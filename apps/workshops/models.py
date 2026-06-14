from django.db import models
from django.conf import settings

class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    workshop_type = models.CharField(max_length=50, choices=[
        ('financial_literacy', 'Financial Literacy'),
        ('legal_rights', 'Legal Rights'),
        ('self_defense', 'Self Defense'),
        ('trauma_healing', 'Trauma Healing'),
        ('digital_safety', 'Digital Safety')
    ])
    is_live = models.BooleanField(default=False)
    meeting_url = models.URLField(blank=True)
    recording_url = models.URLField(blank=True)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, through='WorkshopAttendance')

class WorkshopAttendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    attended_at = models.DateTimeField(auto_now_add=True)
    feedback_rating = models.IntegerField(null=True)
    feedback_text = models.TextField(blank=True)