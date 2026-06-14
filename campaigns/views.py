from rest_framework import viewsets, permissions
from .models import AwarenessCampaign
from .serializers import AwarenessCampaignSerializer

class AwarenessCampaignViewSet(viewsets.ModelViewSet):
    serializer_class = AwarenessCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'organisation'):
            return AwarenessCampaign.objects.filter(organisation=self.request.user.organisation)
        return AwarenessCampaign.objects.none()
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'organisation'):
            serializer.save(organisation=self.request.user.organisation)
