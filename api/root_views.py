from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class RootAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'Welcome to AmakaziWatch API',
            'version': '3.0.0',
            'endpoints': {
                'swagger': '/swagger/',
                'redoc': '/redoc/',
                'api': '/api/',
                'admin': '/admin/',
                'auth': '/api/auth/',
                'reports': '/api/reports/',
                'organisations': '/api/organisations/',
                'safety': '/api/safety/',
                'vault': '/api/vault/',
                'peer': '/api/peer/',
                'legal': '/api/legal/',
                'terms': '/api/terms/',
                'privacy': '/api/privacy-policy/',
            }
        })
