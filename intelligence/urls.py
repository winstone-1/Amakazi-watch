from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIKeyViewSet, APIUsageLogViewSet

router = DefaultRouter()
router.register(r'keys', APIKeyViewSet, basename='api-key')
router.register(r'logs', APIUsageLogViewSet, basename='api-log')

urlpatterns = [
    path('', include(router.urls)),
]
