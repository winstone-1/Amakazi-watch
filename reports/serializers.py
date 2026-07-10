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

    def create(self, validated_data):
        # Remove id if it somehow gets in
        validated_data.pop('id', None)
        # Remove user if it's in there (view handles it)
        validated_data.pop('user', None)
        return IncidentReport.objects.create(**validated_data)

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
