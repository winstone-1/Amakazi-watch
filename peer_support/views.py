from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PeerSupporter, PeerSupportSession
from .serializers import PeerSupporterSerializer, PeerSupportSessionSerializer

class PeerSupporterViewSet(viewsets.ModelViewSet):
    queryset = PeerSupporter.objects.all()
    serializer_class = PeerSupporterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PeerSupportSessionViewSet(viewsets.ModelViewSet):
    queryset = PeerSupportSession.objects.all()
    serializer_class = PeerSupportSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
