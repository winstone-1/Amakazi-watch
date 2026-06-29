from django.db import models

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('reporting', 'Reporting'),
        ('safety', 'Safety'),
        ('legal', 'Legal Rights'),
        ('organisations', 'Organisations'),
        ('account', 'Account'),
    ]
    
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.question[:50]
