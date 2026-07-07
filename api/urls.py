from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageSwitchView, ProfileView, PanicAlertView, health_check
from .admin_views import AdminUserViewSet, AdminOrganisationViewSet, AdminReportViewSet
from .terms_views import TermsOfServiceView, AcceptTermsView

router = DefaultRouter()
router.register(r'admin/users', AdminUserViewSet, basename='admin-users')
router.register(r'admin/organisations', AdminOrganisationViewSet, basename='admin-orgs')
router.register(r'admin/reports', AdminReportViewSet, basename='admin-reports')

urlpatterns = [
    # Health check (must be at root of api)
    path('health/', health_check, name='health_check'),
    
    # Other endpoints
    path('language/', LanguageSwitchView.as_view(), name='language-switch'),
    path('auth/', include('users.urls')),
    path('reports/', include('reports.urls')),
    path('organisations/', include('organisations.urls')),
    path('content/', include('content.urls')),
    path('safety/', include('safety.urls')),
    path('vault/', include('vault.urls')),
    path('peer/', include('peer_support.urls')),
    path('legal/', include('legal_bot.urls')),
    path('org/', include('org_coordination.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('workshops/', include('workshops.urls')),
    path('tips/', include('tips.urls')),
    path('scorecard/', include('county_scorecard.urls')),
    path('notifications/', include('notifications.urls')),
    path('donations/', include('donations.urls')),
    path('licensing/', include('licensing.urls')),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('panic/', PanicAlertView.as_view(), name='panic-alert'),
    path('terms/', TermsOfServiceView.as_view(), name='terms'),
    path('terms/accept/', AcceptTermsView.as_view(), name='terms-accept'),
    path('', include(router.urls)),
]
