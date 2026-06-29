from django.db import models
from django.conf import settings
from organisations.models import Organisation

class ResourceInventory(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=50, choices=[
        ('bed', 'Bed Space'),
        ('legal_slot', 'Legal Aid Slot'),
        ('counselor', 'Counselor Session'),
        ('food_pack', 'Food Pack'),
        ('transport_voucher', 'Transport Voucher')
    ])
    available_count = models.IntegerField()
    total_capacity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

class CaseMatching(models.Model):
    case_ref = models.CharField(max_length=20)
    survivor_needs = models.JSONField()
    matched_organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    match_score = models.FloatField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

class InterOrgMessage(models.Model):
    from_org = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='sent_messages')
    to_org = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    case_ref = models.CharField(max_length=20, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Volunteer(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    hours_this_month = models.IntegerField(default=0)
    background_check_complete = models.BooleanField(default=False)
    training_completed = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

class HotspotAlert(models.Model):
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50)
    predicted_risk_score = models.FloatField()
    reason = models.TextField()
    recommended_actions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
