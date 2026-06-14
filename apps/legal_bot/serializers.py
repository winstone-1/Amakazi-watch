from rest_framework import serializers
from .models import LegalQuery, KenyanLawReference

class LegalQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalQuery
        fields = '__all__'
        read_only_fields = ('created_at',)

class KenyanLawReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KenyanLawReference
        fields = '__all__'
