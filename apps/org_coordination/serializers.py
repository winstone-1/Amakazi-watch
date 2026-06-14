from rest_framework import serializers
from .models import ResourceInventory, CaseMatching, InterOrgMessage, Volunteer, HotspotAlert

class ResourceInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceInventory
        fields = '__all__'
        read_only_fields = ('organisation', 'last_updated')

class CaseMatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseMatching
        fields = '__all__'
        read_only_fields = ('created_at',)

class InterOrgMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterOrgMessage
        fields = '__all__'
        read_only_fields = ('from_org', 'created_at', 'is_read')

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'
        read_only_fields = ('organisation', 'hours_this_month')

class HotspotAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotspotAlert
        fields = '__all__'
