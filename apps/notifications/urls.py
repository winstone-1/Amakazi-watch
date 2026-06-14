from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notifications"),
    path("read-all/", views.NotificationMarkReadView.as_view(), name="notifications-read-all"),
    path("<int:pk>/read/", views.NotificationMarkReadView.as_view(), name="notification-read"),
    path("audit/", views.AuditLogListView.as_view(), name="audit-log"),
]
