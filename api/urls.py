from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema, extend_schema_view
from . import views

TokenObtainPairView = extend_schema_view(
    post=extend_schema(
        tags=['Auth'],
        summary='Obtain JWT access and refresh tokens',
    )
)(TokenObtainPairView)

TokenRefreshView = extend_schema_view(
    post=extend_schema(
        tags=['Auth'],
        summary='Refresh JWT access token',
    )
)(TokenRefreshView)

urlpatterns = [
    # Reports
    path("reports/", views.ReportCreateView.as_view(), name="report-create"),
    path("reports/heatmap/", views.HeatmapView.as_view(), name="heatmap"),
    path("reports/stats/", views.ReportStatsView.as_view(), name="report-stats"),

    # Organisations
    path("organisations/", views.OrganisationListView.as_view(), name="org-list"),
    path("organisations/register/", views.OrganisationRegisterView.as_view(), name="org-register"),
    path("organisations/map/", views.OrganisationsGeoJSONView.as_view(), name="org-map"),
    path("organisations/heatmap/", views.HeatmapGeoJSONView.as_view(), name="org-heatmap"),
    path("organisations/<int:pk>/impact/", views.OrganisationImpactView.as_view(), name="org-impact"),
    path("organisations/<int:pk>/bookmark/", views.BookmarkOrgView.as_view(), name="org-bookmark"),

    # Content
    path("content/", views.ContentListView.as_view(), name="content-list"),
    path("content/create/", views.ContentCreateView.as_view(), name="content-create"),
    path("content/featured/", views.FeaturedContentView.as_view(), name="content-featured"),
    path("content/videos/", views.YoutubeVideosView.as_view(), name="youtube-videos"),

    # Quizzes
    path("quizzes/", views.QuizListView.as_view(), name="quiz-list"),
    path("quizzes/<int:pk>/complete/", views.QuizCompleteView.as_view(), name="quiz-complete"),

    # Donations
    path("donations/initiate/", views.DonationInitiateView.as_view(), name="donation-initiate"),
    path("donations/verify/", views.DonationVerifyView.as_view(), name="donation-verify"),

    # Analytics
    path("analytics/county-summary/", views.CountySummaryExportView.as_view(), name="county-summary"),
    path("analytics/trend/", views.TrendReportExportView.as_view(), name="trend-report"),
    path("analytics/county-official/", views.CountyOfficialHeatmapView.as_view(), name="county-official-heatmap"),

    # Search
    path("search/", views.SearchView.as_view(), name="search"),

    # Profile
    path("profile/", views.ProfileView.as_view(), name="profile"),

    # Referrals
    path("referrals/", views.ReferralCreateView.as_view(), name="referral-create"),
    path("referrals/list/", views.ReferralListView.as_view(), name="referral-list"),
    path("referrals/<int:pk>/", views.ReferralUpdateView.as_view(), name="referral-update"),

    # Case Tracking
    path("cases/<str:ref_code>/", views.CaseTrackingView.as_view(), name="case-tracking"),

    # WhatsApp Bot
    path("whatsapp/webhook/", views.WhatsAppWebhookView.as_view(), name="whatsapp-webhook"),

    # Voice Reporting
    path("voice/callback/", views.VoiceReportCallbackView.as_view(), name="voice-callback"),
    path("voice/reports/", views.VoiceReportListView.as_view(), name="voice-reports"),

    # Ratings and Reviews
    path("content/<int:pk>/rate/", views.ContentRatingView.as_view(), name="content-rate"),
    path("organisations/<int:pk>/reviews/", views.OrganisationReviewView.as_view(), name="org-reviews"),

    # Panic Button
    path("panic/contacts/", views.EmergencyContactListView.as_view(), name="emergency-contacts"),
    path("panic/contacts/<int:pk>/", views.EmergencyContactDeleteView.as_view(), name="emergency-contact-delete"),
    path("panic/", views.PanicButtonView.as_view(), name="panic-button"),

    # Chat
    path("chat/", views.ChatView.as_view(), name="chat"),

    # Password Reset
    path("auth/password-reset/", views.PasswordResetRequestView.as_view(), name="password-reset"),
    path("auth/password-reset/confirm/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("auth/password-change/", views.PasswordChangeView.as_view(), name="password-change"),

    # Two Factor Auth
    path("auth/2fa/setup/", views.TwoFactorSetupView.as_view(), name="2fa-setup"),
    path("auth/2fa/verify/", views.TwoFactorVerifyView.as_view(), name="2fa-verify"),
    path("auth/2fa/disable/", views.TwoFactorDisableView.as_view(), name="2fa-disable"),

    path("auth/google/callback/", views.GoogleAuthCallbackView.as_view(), name="google-callback"),

    # Auth
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
