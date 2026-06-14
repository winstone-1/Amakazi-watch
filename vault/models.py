from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

secure_storage = FileSystemStorage(location='/secure_vault/')

class EvidenceDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(storage=secure_storage)
    file_type = models.CharField(max_length=20, choices=[
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('screenshot', 'Screenshot')
    ])
    description = models.TextField()
    incident_date = models.DateTimeField()
    metadata_json = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_court_admissible = models.BooleanField(default=False)