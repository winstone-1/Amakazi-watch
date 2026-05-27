from rest_framework import serializers
from reports.models import IncidentReport
from organisations.models import Organisation, Donation
from content.models import EducationContent, Quiz
from users.models import User


class IncidentReportSerializer(serializers.ModelSerializer):
    evidence_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model  = IncidentReport
        fields = [
            'id', 'abuse_type', 'relationship', 'county',
            'sub_county', 'description', 'evidence_url',
            'evidence_file', 'sms_ref_code', 'urgency_score',
            'flagged_for_review', 'created_at'
        ]
        read_only_fields = [
            'id', 'sms_ref_code', 'urgency_score',
            'flagged_for_review', 'created_at', 'evidence_url'
        ]

    def create(self, validated_data):
        from reports.utils.upload import upload_evidence
        evidence_file = validated_data.pop('evidence_file', None)
        report = IncidentReport(**validated_data)
        if evidence_file:
            result = upload_evidence(evidence_file, folder='evidence')
            if result['success']:
                report.evidence_url = result['url']
        report.save()
        return report


class OrganisationSerializer(serializers.ModelSerializer):
    document_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model  = Organisation
        fields = [
            'id', 'name', 'description', 'services', 'county',
            'sub_county', 'phone', 'email', 'website',
            'latitude', 'longitude', 'document_url',
            'document_file', 'verified', 'created_at'
        ]
        read_only_fields = ['verified', 'created_at', 'document_url']

    def create(self, validated_data):
        from reports.utils.upload import upload_evidence
        document_file = validated_data.pop('document_file', None)
        org = Organisation(**validated_data)
        if document_file:
            result = upload_evidence(document_file, folder='org_documents')
            if result['success']:
                org.document_url = result['url']
        org.save()
        return org


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Donation
        fields = ['id', 'organisation', 'amount', 'phone', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class EducationContentSerializer(serializers.ModelSerializer):
    organisation_name = serializers.CharField(source='organisation.name', read_only=True)
    pdf_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model  = EducationContent
        fields = [
            'id', 'title', 'body', 'format', 'topic',
            'organisation', 'organisation_name',
            'youtube_url', 'pdf_url', 'pdf_file',
            'approved', 'created_at'
        ]
        read_only_fields = ['approved', 'created_at', 'pdf_url']

    def create(self, validated_data):
        from reports.utils.upload import upload_evidence
        pdf_file = validated_data.pop('pdf_file', None)
        content = EducationContent(**validated_data)
        if pdf_file:
            result = upload_evidence(pdf_file, folder='guides')
            if result['success']:
                content.pdf_url = result['url']
        content.save()
        return content


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
