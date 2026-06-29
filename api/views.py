from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import translation
from django.contrib.auth import get_user_model

User = get_user_model()

class LanguageSwitchView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        language = request.data.get('language', 'en')
        if language in ['en', 'sw']:
            translation.activate(language)
            request.session['django_language'] = language
            return Response({'message': f'Language switched to {language}', 'language': language})
        return Response({'error': 'Language must be en or sw'}, status=400)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': getattr(user, 'role', 'survivor'),
            'phone': getattr(user, 'phone', ''),
            'county': getattr(user, 'county', ''),
            'bio': getattr(user, 'bio', ''),
        })
    
    def patch(self, request):
        user = request.user
        allowed_fields = ['phone', 'county', 'bio', 'role']
        for key, value in request.data.items():
            if key in allowed_fields and hasattr(user, key):
                setattr(user, key, value)
        user.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': getattr(user, 'role', 'survivor'),
            'phone': getattr(user, 'phone', ''),
            'county': getattr(user, 'county', ''),
            'bio': getattr(user, 'bio', ''),
        })
