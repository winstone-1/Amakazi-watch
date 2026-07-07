from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LegalQuery, KenyanLawReference
from .serializers import LegalQuerySerializer, KenyanLawReferenceSerializer

class LegalQueryViewSet(viewsets.ModelViewSet):
    queryset = LegalQuery.objects.all()
    serializer_class = LegalQuerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class KenyanLawReferenceViewSet(viewsets.ModelViewSet):
    queryset = KenyanLawReference.objects.all()
    serializer_class = KenyanLawReferenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
