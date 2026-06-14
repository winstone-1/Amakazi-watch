from django.db import models

class LegalQuery(models.Model):
    session_id = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    law_citations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
class KenyanLawReference(models.Model):
    law_name = models.CharField(max_length=200)
    section = models.CharField(max_length=50)
    summary = models.TextField()
    keywords = models.JSONField(default=list)
    full_text_url = models.URLField(blank=True)