from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Count
from .models import IncidentReport
from .serializers import IncidentReportSerializer
from api.logging import log_action


@extend_schema(exclude=True)
class IncidentReportListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        reports = IncidentReport.objects.filter(user=request.user) if request.user.is_authenticated else IncidentReport.objects.none()
        serializer = IncidentReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a mutable copy of request data
        data = request.data.copy()
        
        # Remove user from data if present (it will be set by the view)
        data.pop('user', None)
        
        # Set default values if missing
        if 'is_anonymous' not in data:
            data['is_anonymous'] = True
        if 'status' not in data:
            data['status'] = 'pending'
        
        serializer = IncidentReportSerializer(data=data)
        
        if serializer.is_valid():
            # Save with user from request
            report = serializer.save(
                user=request.user if request.user.is_authenticated else None
            )
            log_action('report_submission', user=request.user if request.user.is_authenticated else None, 
                      details={'report_id': report.id, 'abuse_type': report.abuse_type})
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


@extend_schema(exclude=True)
class ReportStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        stats = {
            'total_reports': IncidentReport.objects.count(),
            'abuse_types': list(IncidentReport.objects.values('abuse_type').annotate(count=Count('id'))),
        }
        return Response(stats)
