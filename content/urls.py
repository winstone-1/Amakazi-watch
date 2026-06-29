from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
try:
    router.register(r'', views.ContentViewSet, basename='content')
except:
    pass

urlpatterns = [
    path('', include(router.urls)),
]
