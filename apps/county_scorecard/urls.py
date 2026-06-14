from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountyScorecardViewSet

router = DefaultRouter()
router.register(r'', CountyScorecardViewSet, basename='scorecard')

urlpatterns = [
    path('', include(router.urls)),
]
