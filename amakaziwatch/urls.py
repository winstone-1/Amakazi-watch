from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from reports.views import home

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AmakaziWatch API",
        default_version='v3',
        description="Kenya's first crowdsourced GBV awareness, reporting and prevention platform",
        terms_of_service="https://www.amakaziwatch.com/terms/",
        contact=openapi.Contact(email="support@amakaziwatch.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/", include("api.urls")),
    path("api/subscriptions/", include("subscriptions.urls")),
    path("api/intelligence/", include("intelligence.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
