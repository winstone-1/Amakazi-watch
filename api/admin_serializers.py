from rest_framework import serializers
from users.models import User
from organisations.models import Organisation
from reports.models import IncidentReport

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'county', 'is_staff', 'is_active', 'date_joined']

class AdminOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class AdminReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = '__all__'
