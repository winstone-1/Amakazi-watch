from rest_framework import serializers
from .models import AwarenessCampaign

class AwarenessCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessCampaign
        fields = '__all__'
        read_only_fields = ('organisation', 'sent_at', 'delivery_stats')
