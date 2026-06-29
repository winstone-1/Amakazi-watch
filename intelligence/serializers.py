from rest_framework import serializers
from .models import APIKey, APIUsageLog

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'
        read_only_fields = ['key', 'requests_this_month', 'created_at']

class APIUsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIUsageLog
        fields = '__all__'
