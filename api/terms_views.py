from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .terms_models import TermsOfService, UserTermsAcceptance

@extend_schema(exclude=True)
class TermsOfServiceView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        language = request.headers.get('Accept-Language', 'en')
        terms = TermsOfService.objects.filter(is_active=True).first()
        if terms:
            return Response({
                'version': terms.version,
                'content': terms.get_content(language),
                'effective_date': terms.effective_date,
                'language': language
            })
        return Response({'error': 'Terms not found'}, status=404)

@extend_schema(exclude=True)
class AcceptTermsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        language = request.headers.get('Accept-Language', 'en')
        terms = TermsOfService.objects.filter(is_active=True).first()
        if not terms:
            return Response({'error': 'No active terms'}, status=404)
        
        acceptance, created = UserTermsAcceptance.objects.get_or_create(
            user=request.user,
            terms_version=terms,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'language': language
            }
        )
        return Response({
            'message': f'Terms v{terms.version} accepted',
            'language': language
        })
