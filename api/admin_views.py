from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count
from reports.models import IncidentReport
from organisations.models import Organisation

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class AdminUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = {
            'total_users': User.objects.count(),
            'total_reports': IncidentReport.objects.count(),
            'total_organisations': Organisation.objects.count(),
            'users_by_role': list(User.objects.values('role').annotate(count=Count('id')))
        }
        return Response(stats)

class AdminOrganisationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Organisation.objects.all()
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        org = self.get_object()
        org.is_verified = True
        org.save()
        return Response({'message': f'Organisation {org.name} verified'})

class AdminReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = IncidentReport.objects.all()
