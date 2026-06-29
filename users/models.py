from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('survivor', 'Survivor'),
        ('counselor', 'Counselor'),
        ('org_staff', 'Organization Staff'),
        ('county_official', 'County Official'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='survivor')
    phone = models.CharField(max_length=15, blank=True)
    county = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
