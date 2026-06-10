from django.urls import path
from . import views

urlpatterns = [
    path("plans/", views.PlansView.as_view(), name="subscription-plans"),
    path("<int:org_id>/status/", views.SubscriptionStatusView.as_view(), name="subscription-status"),
    path("<int:org_id>/upgrade/", views.SubscriptionUpgradeView.as_view(), name="subscription-upgrade"),
    path("<int:org_id>/verify/", views.SubscriptionVerifyView.as_view(), name="subscription-verify"),
]
