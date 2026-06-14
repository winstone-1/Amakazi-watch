from rest_framework import serializers
from .models import Workshop, WorkshopAttendance

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'

class WorkshopAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopAttendance
        fields = '__all__'
        read_only_fields = ('user', 'attended_at')
