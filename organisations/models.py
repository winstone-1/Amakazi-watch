from django.db import models

class Organisation(models.Model):
    ORG_TYPES = [
        ('ngo', 'NGO'),
        ('cbo', 'Community Based Organization'),
        ('faith', 'Faith Based Organization'),
        ('government', 'Government Agency'),
        ('legal', 'Legal Aid'),
        ('shelter', 'Shelter'),
        ('health', 'Health Facility'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    org_type = models.CharField(max_length=20, choices=ORG_TYPES, default='ngo')
    description = models.TextField(blank=True)
    services = models.TextField(blank=True, help_text='Comma separated list of services')
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
