from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import AnonymousTip
from .serializers import AnonymousTipSerializer

class AnonymousTipViewSet(viewsets.ModelViewSet):
    serializer_class = AnonymousTipSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # Only staff can view tips
        if self.request.user.is_staff:
            return AnonymousTip.objects.all()
        return AnonymousTip.objects.none()
    
    def perform_create(self, serializer):
        serializer.save()
        # Trigger alert if urgent
        if serializer.instance.is_urgent:
            # Send notification to nearest orgs
            pass
