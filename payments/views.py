from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer
import uuid

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def initiate(self, request):
        amount = request.data.get('amount')
        method = request.data.get('payment_method', 'mpesa')
        
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            reference=uuid.uuid4().hex[:12].upper(),
            payment_method=method,
            status='pending'
        )
        
        return Response({
            'payment': PaymentSerializer(payment).data,
            'message': 'Payment initiated. Please complete payment.'
        })
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'completed'
        payment.completed_at = timezone.now()
        payment.save()
        return Response({'message': 'Payment verified successfully'})
