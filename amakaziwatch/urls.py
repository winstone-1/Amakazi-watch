from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home(request):
    return JsonResponse({
        'message': 'AmakaziWatch API is running!',
        'docs': '/docs/',
        'admin': '/admin/'
    })

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui-docs"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
