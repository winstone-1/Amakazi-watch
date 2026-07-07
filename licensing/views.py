from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class LicensingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Licensing endpoint available', 'user': request.user.id})

    def post(self, request):
        return Response({'message': 'License request received', 'organization': request.data.get('organization')})
