from django.db import models
from django.conf import settings
from django.utils import timezone

class Plan(models.Model):
    PLAN_TYPES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=20, choices=PLAN_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_name_display()} - KES {self.price}"

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=timezone.now)  # Added default
    payment_reference = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

class SubscriptionPayment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
