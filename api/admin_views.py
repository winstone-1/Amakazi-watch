from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from users.models import User
from organisations.models import Organisation
from reports.models import IncidentReport
from .admin_serializers import AdminUserSerializer, AdminOrganisationSerializer, AdminReportSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

class AdminOrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = AdminOrganisationSerializer
    permission_classes = [IsAdminUser]

class AdminReportViewSet(viewsets.ModelViewSet):
    queryset = IncidentReport.objects.all()
    serializer_class = AdminReportSerializer
    permission_classes = [IsAdminUser]
