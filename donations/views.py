from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Donation
from .serializers import DonationSerializer
import uuid

class DonationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        donations = Donation.objects.filter(user=request.user)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

class InitiateDonationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        amount = request.data.get('amount')
        organisation_id = request.data.get('organisation_id')
        email = request.data.get('email', '')
        phone = request.data.get('phone', '')
        
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        donation = Donation.objects.create(
            user=request.user,
            amount=amount,
            organisation_id=organisation_id,
            email=email,
            phone=phone,
            reference=uuid.uuid4().hex[:12].upper(),
            status='pending'
        )
        
        return Response({
            'donation': DonationSerializer(donation).data,
            'message': 'Donation initiated. Please complete payment.',
            'checkout_request_id': f'CHECKOUT_{donation.id}'
        }, status=status.HTTP_201_CREATED)

class VerifyDonationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        reference = request.query_params.get('reference')
        if not reference:
            return Response({'error': 'Reference is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            donation = Donation.objects.get(reference=reference)
            donation.status = 'completed'
            donation.save()
            return Response({
                'message': 'Donation verified successfully',
                'donation': DonationSerializer(donation).data
            })
        except Donation.DoesNotExist:
            return Response({'error': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)
