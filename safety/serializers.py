from rest_framework import serializers
from .models import SafetyTimer, SafeWord, RiskAssessment, EscapePlan

class SafetyTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyTimer
        fields = '__all__'
        read_only_fields = ('user', 'start_time', 'status')

class SafeWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafeWord
        fields = ['id', 'code_word', 'is_active', 'created_at']
        read_only_fields = ('user', 'created_at')

class RiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessment
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class EscapePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscapePlan
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
