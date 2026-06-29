from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageSwitchView

urlpatterns = [
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
]
from .admin_views import AdminUserViewSet, AdminOrganisationViewSet, AdminReportViewSet

router = DefaultRouter()
router.register(r'admin/users', AdminUserViewSet, basename='admin-users')
router.register(r'admin/organisations', AdminOrganisationViewSet, basename='admin-orgs')
router.register(r'admin/reports', AdminReportViewSet, basename='admin-reports')

urlpatterns += [
    path('', include(router.urls)),
]
from .terms_views import TermsOfServiceView, AcceptTermsView

urlpatterns += [
    path('terms/', TermsOfServiceView.as_view(), name='terms'),
    path('terms/accept/', AcceptTermsView.as_view(), name='terms-accept'),
]
# Add new app URLs
urlpatterns += [
    path('notifications/', include('notifications.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('intelligence/', include('intelligence.urls')),
    path('faq/', include('faq.urls')),
    path('resources/', include('resources.urls')),
    path('stories/', include('stories.urls')),
    path('payments/', include('payments.urls')),
]
