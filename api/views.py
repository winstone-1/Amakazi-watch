from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext as _
from django.utils import translation

class LanguageSwitchView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        language = request.data.get('language', 'en')
        if language in ['en', 'sw']:
            translation.activate(language)
            request.session['django_language'] = language
            return Response({'message': f'Language switched to {language}', 'language': language})
        return Response({'error': 'Language must be en or sw'}, status=400)
