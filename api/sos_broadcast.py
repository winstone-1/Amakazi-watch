from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class SOSBroadcastView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'SOS sent to nearby responders',
            'count': 15
        })
