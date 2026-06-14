from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceInventoryViewSet, CaseMatchingViewSet, InterOrgMessageViewSet, VolunteerViewSet, HotspotAlertViewSet

router = DefaultRouter()
router.register(r'inventory', ResourceInventoryViewSet, basename='org-inventory')
router.register(r'case-matching', CaseMatchingViewSet, basename='case-matching')
router.register(r'messages', InterOrgMessageViewSet, basename='org-messages')
router.register(r'volunteers', VolunteerViewSet, basename='volunteers')
router.register(r'hotspots', HotspotAlertViewSet, basename='hotspots')

urlpatterns = [
    path('', include(router.urls)),
]
