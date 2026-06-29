from django.db import models

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('safety_plan', 'Safety Plan'),
        ('legal_handbook', 'Legal Handbook'),
        ('emergency_cards', 'Emergency Cards'),
        ('self_care', 'Self Care'),
        ('video', 'Video Tutorial'),
        ('guide', 'Guide'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    file_url = models.URLField(blank=True)
    content = models.TextField(blank=True)
    is_downloadable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
