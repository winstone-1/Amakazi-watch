from rest_framework import serializers
from .models import ResourceInventory, CaseMatching, InterOrgMessage, Volunteer, HotspotAlert

class ResourceInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceInventory
        fields = '__all__'

class CaseMatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseMatching
        fields = '__all__'

class InterOrgMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterOrgMessage
        fields = '__all__'

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

class HotspotAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotspotAlert
        fields = '__all__'
