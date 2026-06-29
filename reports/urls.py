from django.urls import path
from .views import IncidentReportListView, ReportStatsView

urlpatterns = [
    path('', IncidentReportListView.as_view(), name='report-list'),
    path('stats/', ReportStatsView.as_view(), name='report-stats'),
]
