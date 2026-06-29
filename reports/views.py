from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Count
from .models import IncidentReport

def home(request):
    return Response({"message": "Reports API", "endpoints": ["/stats/", "/"]})

class ReportStatsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        stats = {
            'total_reports': IncidentReport.objects.count(),
            'abuse_types': list(IncidentReport.objects.values('abuse_type').annotate(count=Count('id'))),
            'counties': list(IncidentReport.objects.values('county').annotate(count=Count('id'))[:5])
        }
        return Response(stats)

class ReportCreateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        return Response({"message": "Report created"})
