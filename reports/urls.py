from django.urls import path
from .views import ReportStatsView, ReportCreateView

urlpatterns = [
    path('stats/', ReportStatsView.as_view(), name='report-stats'),
    path('', ReportCreateView.as_view(), name='report-create'),
]
