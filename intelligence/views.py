from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import APIKey, APIUsageLog
from .serializers import APIKeySerializer, APIUsageLogSerializer
import uuid

class APIKeyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = APIKeySerializer
    
    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        key = uuid.uuid4().hex[:32]
        serializer.save(user=self.request.user, key=key)

class APIUsageLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = APIUsageLogSerializer
    
    def get_queryset(self):
        return APIUsageLog.objects.filter(api_key__user=self.request.user)
