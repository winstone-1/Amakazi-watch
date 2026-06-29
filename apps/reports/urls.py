from django.urls import path
from .views import ReportStatsView

urlpatterns = [
    path('stats/', ReportStatsView.as_view(), name='report-stats'),
]
