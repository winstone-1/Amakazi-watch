from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeerSupporterViewSet, PeerSupportSessionViewSet

router = DefaultRouter()
router.register(r'supporters', PeerSupporterViewSet, basename='peer-supporter')
router.register(r'sessions', PeerSupportSessionViewSet, basename='peer-session')

urlpatterns = [
    path('', include(router.urls)),
]
