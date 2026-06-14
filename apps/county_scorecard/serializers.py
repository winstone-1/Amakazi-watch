from rest_framework import serializers
from .models import CountyScorecard, ScorecardHistory

class CountyScorecardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountyScorecard
        fields = '__all__'

class ScorecardHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScorecardHistory
        fields = '__all__'
