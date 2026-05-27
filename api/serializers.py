from rest_framework import serializers
from reports.models import IncidentReport
from organisations.models import Organisation, Donation
from content.models import EducationContent, Quiz
from users.models import User


class IncidentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model  = IncidentReport
        fields = [
            'id', 'abuse_type', 'relationship', 'county',
            'sub_county', 'description', 'evidence_url',
            'sms_ref_code', 'urgency_score', 'flagged_for_review',
            'created_at'
        ]
        read_only_fields = ['id', 'sms_ref_code', 'urgency_score', 'flagged_for_review', 'created_at']


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Organisation
        fields = [
            'id', 'name', 'description', 'services', 'county',
            'sub_county', 'phone', 'email', 'website',
            'latitude', 'longitude', 'document_url', 'verified', 'created_at'
        ]
        read_only_fields = ['verified', 'created_at']


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Donation
        fields = ['id', 'organisation', 'amount', 'phone', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class EducationContentSerializer(serializers.ModelSerializer):
    organisation_name = serializers.CharField(source='organisation.name', read_only=True)

    class Meta:
        model  = EducationContent
        fields = [
            'id', 'title', 'body', 'format', 'topic',
            'organisation', 'organisation_name',
            'youtube_url', 'pdf_url', 'approved', 'created_at'
        ]
        read_only_fields = ['approved', 'created_at']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Quiz
        fields = [
            'id', 'title', 'topic', 'organisation',
            'questions', 'approved', 'completion_count', 'created_at'
        ]
        read_only_fields = ['approved', 'completion_count', 'created_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
