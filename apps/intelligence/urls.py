from django.urls import path
from . import views

urlpatterns = [
    path("keys/", views.APIKeyListView.as_view(), name="api-key-list"),
    path("keys/create/", views.APIKeyCreateView.as_view(), name="api-key-create"),
    path("county-risk/", views.CountyRiskScoreView.as_view(), name="county-risk"),
    path("abuse-distribution/", views.AbuseTypeDistributionView.as_view(), name="abuse-distribution"),
    path("trend-forecast/", views.TrendForecastView.as_view(), name="trend-forecast"),
]
