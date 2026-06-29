from django.db import models
from django.conf import settings

class Story(models.Model):
    CATEGORY_CHOICES = [
        ('survivor', 'Survivor Story'),
        ('organization', 'Organization Impact'),
        ('counselor', 'Counselor Experience'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_anonymous = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='survivor')
    is_approved = models.BooleanField(default=False)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
