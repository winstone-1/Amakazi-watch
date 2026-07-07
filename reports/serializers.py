import uuid
from rest_framework import serializers
from django.db import connection
from .models import IncidentReport, Report


class IncidentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = (
            'id',
            'user',
            'abuse_type',
            'relationship',
            'county',
            'sub_county',
            'description',
            'phone',
            'is_anonymous',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        phone = validated_data.pop('phone', None)
        is_anonymous = validated_data.pop('is_anonymous', None)
        status = validated_data.pop('status', None)
        report_id = str(uuid.uuid4())
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO reports_incidentreport (
                    id, abuse_type, relationship, county, sub_county, description,
                    evidence_url, sms_ref_code, urgency_score, ai_classification,
                    flagged_for_review, created_at, user_id, phone, is_anonymous, status, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, NOW())
                """,
                [
                    report_id,
                    validated_data['abuse_type'],
                    validated_data['relationship'],
                    validated_data['county'],
                    validated_data.get('sub_county', ''),
                    validated_data['description'],
                    '',
                    '',
                    0,
                    '',
                    False,
                    getattr(user, 'id', None),
                    phone or '',
                    bool(is_anonymous),
                    status or 'pending',
                ],
            )
        return type('CreatedReport', (), {'id': report_id, 'abuse_type': validated_data['abuse_type'], 'user': user, 'county': validated_data['county'], 'sub_county': validated_data.get('sub_county', ''), 'description': validated_data['description'], 'phone': phone or '', 'is_anonymous': bool(is_anonymous), 'status': status or 'pending', 'relationship': validated_data['relationship']})


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
