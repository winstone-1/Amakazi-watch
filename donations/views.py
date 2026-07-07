from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class DonationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Donations endpoint available', 'user': request.user.id})

    def post(self, request):
        return Response({'message': 'Donation initiation queued', 'amount': request.data.get('amount')})
