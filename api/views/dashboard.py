
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from reports.models import Report
from organisations.models import Organisation

class DashboardSummaryView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        stats = {
            'total_reports': Report.objects.count(),
            'reports_this_week': Report.objects.filter(created_at__date__gte=week_ago).count(),
            'active_organisations': Organisation.objects.filter(is_verified=True).count(),
            'abuse_type_breakdown': list(
                Report.objects.values('abuse_type').annotate(count=Count('id'))
            ),
            'top_counties': list(
                Report.objects.values('county').annotate(count=Count('id')).order_by('-count')[:5]
            ),
            'recent_trend': list(
                Report.objects.filter(created_at__date__gte=week_ago)
                .extra({'date': "date(created_at)"})
                .values('date').annotate(count=Count('id'))
                .order_by('date')
            )
        }
        return Response(stats)
