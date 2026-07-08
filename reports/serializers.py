from rest_framework import serializers
from .models import IncidentReport, Report

class IncidentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = [
            'id', 'user', 'abuse_type', 'relationship', 'county', 
            'sub_county', 'description', 'phone', 'is_anonymous', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
