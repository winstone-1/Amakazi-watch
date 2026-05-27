from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Reports
    path('reports/', views.ReportCreateView.as_view(), name='report-create'),
    path('reports/heatmap/', views.HeatmapView.as_view(), name='heatmap'),

    # Organisations
    path('organisations/', views.OrganisationListView.as_view(), name='org-list'),
    path('organisations/register/', views.OrganisationRegisterView.as_view(), name='org-register'),

    # Content
    path('content/', views.ContentListView.as_view(), name='content-list'),
    path('content/create/', views.ContentCreateView.as_view(), name='content-create'),

    # Quizzes
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/complete/', views.QuizCompleteView.as_view(), name='quiz-complete'),

    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
