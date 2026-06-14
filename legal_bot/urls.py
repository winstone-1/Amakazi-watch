from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LegalQueryViewSet, KenyanLawReferenceViewSet

router = DefaultRouter()
router.register(r'ask', LegalQueryViewSet, basename='legal-query')
router.register(r'reference', KenyanLawReferenceViewSet, basename='legal-reference')

urlpatterns = [
    path('', include(router.urls)),
]
