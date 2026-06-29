from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Count
from .models import Report

class ReportStatsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        stats = {
            'total_reports': Report.objects.count(),
            'abuse_types': list(Report.objects.values('abuse_type').annotate(count=Count('id'))),
            'counties': list(Report.objects.values('county').annotate(count=Count('id'))[:5])
        }
        return Response(stats)
