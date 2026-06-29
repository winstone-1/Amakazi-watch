from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count
from .models import IncidentReport, Report
from .serializers import IncidentReportSerializer, ReportSerializer

class IncidentReportListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        reports = IncidentReport.objects.all()
        if request.user.is_authenticated:
            reports = reports.filter(user=request.user)
        serializer = IncidentReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = IncidentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user if request.user.is_authenticated else None)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ReportStatsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        stats = {
            'total_reports': IncidentReport.objects.count(),
            'abuse_types': list(IncidentReport.objects.values('abuse_type').annotate(count=Count('id'))),
        }
        return Response(stats)
