from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .models import EvidenceDocument
from .serializers import EvidenceDocumentSerializer

class EvidenceDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = EvidenceDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EvidenceDocument.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        doc = self.get_object()
        return FileResponse(doc.file, as_attachment=True)
