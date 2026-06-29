from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Plan, Subscription, SubscriptionPayment
from .serializers import PlanSerializer, SubscriptionSerializer, SubscriptionPaymentSerializer

class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class SubscriptionPaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionPaymentSerializer
    
    def get_queryset(self):
        return SubscriptionPayment.objects.filter(subscription__user=self.request.user)
