from django.db import models
from django.conf import settings

class PeerSupporter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_trained = models.BooleanField(default=False)
    training_certified_date = models.DateField(null=True)
    languages = models.JSONField(default=list)
    counties = models.JSONField(default=list)
    max_active_sessions = models.IntegerField(default=3)
    current_sessions = models.IntegerField(default=0)

class PeerSupportSession(models.Model):
    survivor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='peer_sessions')
    supporter = models.ForeignKey(PeerSupporter, on_delete=models.SET_NULL, null=True)
    is_anonymous = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('ended', 'Ended'),
        ('escalated', 'Escalated')
    ])
    messages_json = models.JSONField(default=list)