from rest_framework import serializers
from .models import EvidenceDocument

class EvidenceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceDocument
        fields = ['id', 'file', 'file_type', 'description', 'incident_date', 'metadata_json', 'uploaded_at', 'is_court_admissible']
        read_only_fields = ('user', 'uploaded_at', 'is_court_admissible')
