from django.db import models

class Report(models.Model):
    abuse_type = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
