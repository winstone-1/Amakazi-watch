from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AwarenessCampaignViewSet

router = DefaultRouter()
router.register(r'', AwarenessCampaignViewSet, basename='campaigns')

urlpatterns = [
    path('', include(router.urls)),
]
