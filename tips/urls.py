from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnonymousTipViewSet

router = DefaultRouter()
router.register(r'', AnonymousTipViewSet, basename='tips')

urlpatterns = [
    path('', include(router.urls)),
]
