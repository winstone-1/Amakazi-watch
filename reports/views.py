from django.shortcuts import render
from reports.models import IncidentReport
from organisations.models import Organisation

def home(request):
    total_reports = IncidentReport.objects.count()
    total_orgs    = Organisation.objects.filter(verified=True).count()
    recent_reports = IncidentReport.objects.order_by('-created_at')[:5]

    context = {
        'total_reports': total_reports,
        'total_orgs':    total_orgs,
        'recent_reports': recent_reports,
    }
    return render(request, 'home.html', context)
