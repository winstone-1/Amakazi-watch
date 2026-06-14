from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SafetyTimerViewSet, SafeWordViewSet, RiskAssessmentViewSet, EscapePlanViewSet

router = DefaultRouter()
router.register(r'timer', SafetyTimerViewSet, basename='safety-timer')
router.register(r'safe-word', SafeWordViewSet, basename='safe-word')
router.register(r'risk-assessment', RiskAssessmentViewSet, basename='risk-assessment')
router.register(r'escape-plan', EscapePlanViewSet, basename='escape-plan')

urlpatterns = [
    path('', include(router.urls)),
]
