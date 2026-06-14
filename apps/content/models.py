from django.db import models
from organisations.models import Organisation

class EducationContent(models.Model):
    class Format(models.TextChoices):
        ARTICLE = 'article', 'Article'
        VIDEO   = 'video',   'Video'
        GUIDE   = 'guide',   'Downloadable Guide'

    class Topic(models.TextChoices):
        RECOGNISE  = 'recognise',  'Recognising Abuse'
        LEGAL      = 'legal',      'Legal Rights'
        SUPPORT    = 'support',    'Supporting Survivors'
        HEALTHY    = 'healthy',    'Healthy Relationships'
        PREVENTION = 'prevention', 'Prevention'

    title           = models.CharField(max_length=300)
    body            = models.TextField(blank=True)
    format          = models.CharField(max_length=20, choices=Format.choices)
    topic           = models.CharField(max_length=20, choices=Topic.choices)
    organisation    = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='content')
    youtube_url     = models.URLField(blank=True)
    pdf_url         = models.URLField(blank=True)
    approved        = models.BooleanField(default=False)
    ai_review_notes = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title            = models.CharField(max_length=300)
    topic            = models.CharField(max_length=20, choices=EducationContent.Topic.choices)
    organisation     = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='quizzes')
    questions        = models.JSONField(default=list)
    approved         = models.BooleanField(default=False)
    completion_count = models.IntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContentRating(models.Model):
    content    = models.ForeignKey(EducationContent, on_delete=models.CASCADE, related_name="ratings")
    rating     = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content.title} — {self.rating}/5"
