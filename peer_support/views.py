from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PeerSupporter, PeerSupportSession
from .serializers import *

class PeerSupporterViewSet(viewsets.ModelViewSet):
    serializer_class = PeerSupporterSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PeerSupporter.objects.filter(user=self.request.user)

class PeerSupportSessionViewSet(viewsets.ModelViewSet):
    serializer_class = PeerSupportSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PeerSupportSession.objects.filter(survivor=self.request.user)
    
    @action(detail=False, methods=['post'])
    def find(self, request):
        # Match with available peer supporter
        return Response({'message': 'Peer supporter found'})
    
    @action(detail=True, methods=['post'])
    def message(self, request, pk=None):
        session = self.get_object()
        message = request.data.get('message')
        # Store message in session
        return Response({'message': 'Message sent'})
