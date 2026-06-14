from rest_framework import serializers
from .models import PeerSupporter, PeerSupportSession

class PeerSupporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerSupporter
        fields = '__all__'
        read_only_fields = ('user', 'current_sessions')

class PeerSupportSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerSupportSession
        fields = '__all__'
        read_only_fields = ('survivor', 'started_at')
