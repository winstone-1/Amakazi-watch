from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet, SubscriptionPaymentViewSet

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'payments', SubscriptionPaymentViewSet, basename='subscription-payment')

urlpatterns = [
    path('', include(router.urls)),
]
