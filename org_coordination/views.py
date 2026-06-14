from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ResourceInventory, CaseMatching, InterOrgMessage, Volunteer, HotspotAlert
from .serializers import *

class ResourceInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'organisation'):
            return ResourceInventory.objects.filter(organisation=self.request.user.organisation)
        return ResourceInventory.objects.none()
    
    @action(detail=False, methods=['get'])
    def county(self, request):
        county = request.query_params.get('county')
        # Filter by county through organisation
        return Response({'message': 'Filtered by county'})

class CaseMatchingViewSet(viewsets.ModelViewSet):
    serializer_class = CaseMatchingSerializer
    permission_classes = [permissions.IsAuthenticated]

class InterOrgMessageViewSet(viewsets.ModelViewSet):
    serializer_class = InterOrgMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'organisation'):
            org = self.request.user.organisation
            return InterOrgMessage.objects.filter(from_org=org) | InterOrgMessage.objects.filter(to_org=org)
        return InterOrgMessage.objects.none()
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'organisation'):
            serializer.save(from_org=self.request.user.organisation)

class VolunteerViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'organisation'):
            return Volunteer.objects.filter(organisation=self.request.user.organisation)
        return Volunteer.objects.none()

class HotspotAlertViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotspotAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return HotspotAlert.objects.filter(expires_at__gt=timezone.now())
