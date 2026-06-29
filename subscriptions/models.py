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
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    plan = models.ForeignKey(
        Plan, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username if self.user else 'No user'} - {self.plan.name if self.plan else 'No plan'}"

class SubscriptionPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    subscription = models.ForeignKey(
        Subscription, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True, null=True)  # <-- FIXED: added null=True
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reference or 'No ref'} - {self.status}"
