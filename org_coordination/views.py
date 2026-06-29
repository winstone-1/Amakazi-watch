from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ResourceInventory, CaseMatching, InterOrgMessage, Volunteer, HotspotAlert
from .serializers import (
    ResourceInventorySerializer, CaseMatchingSerializer, 
    InterOrgMessageSerializer, VolunteerSerializer, HotspotAlertSerializer
)

class ResourceInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'organisation'):
            return ResourceInventory.objects.filter(organisation=self.request.user.organisation)
        return ResourceInventory.objects.none()

class CaseMatchingViewSet(viewsets.ModelViewSet):
    serializer_class = CaseMatchingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CaseMatching.objects.all()

class InterOrgMessageViewSet(viewsets.ModelViewSet):
    serializer_class = InterOrgMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'organisation'):
            org = self.request.user.organisation
            return InterOrgMessage.objects.filter(from_org=org) | InterOrgMessage.objects.filter(to_org=org)
        return InterOrgMessage.objects.none()

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
        return HotspotAlert.objects.all()
