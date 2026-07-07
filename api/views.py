from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import translation
from django.utils import timezone
from django.contrib.auth import get_user_model

from api.logging import log_action

User = get_user_model()


class LanguageSwitchView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        language = request.data.get('language', 'en')
        if language in ['en', 'sw']:
            translation.activate(language)
            request.session['django_language'] = language
            log_action('language_switch', user=request.user if request.user.is_authenticated else None, details={'language': language})
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
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': getattr(user, 'role', 'survivor'),
            'phone': getattr(user, 'phone', ''),
            'county': getattr(user, 'county', ''),
            'bio': getattr(user, 'bio', ''),
        })

    def patch(self, request):
        user = request.user
        allowed_fields = ['phone', 'county', 'bio', 'role', 'first_name', 'last_name']
        for key, value in request.data.items():
            if key in allowed_fields and hasattr(user, key):
                setattr(user, key, value)
        user.save()
        log_action('profile_update', user=user, details={'fields': list(request.data.keys())})
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': getattr(user, 'role', 'survivor'),
            'phone': getattr(user, 'phone', ''),
            'county': getattr(user, 'county', ''),
            'bio': getattr(user, 'bio', ''),
        })


class PanicAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from users.panic import send_panic_alert
        result = send_panic_alert(request.user, location=request.data.get('location'))
        log_action('panic_alert', user=request.user, details={'location': request.data.get('location')})
        return Response(result)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint for Render"""
    return Response({
        'status': 'ok',
        'timestamp': timezone.now().isoformat(),
        'service': 'AmakaziWatch API'
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    phone = request.data.get('phone', '')
    county = request.data.get('county', '')
    
    if not username or not email or not password:
        return Response({'error': 'Username, email and password required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        phone=phone,
        county=county
    )
    return Response({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'county': user.county,
            'role': user.role
        }
    }, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get user profile"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'county': user.county,
        'role': user.role,
        'bio': user.bio,
        'date_joined': user.date_joined
    })


@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Welcome to AmakaziWatch API',
        'endpoints': {
            'health': '/api/health/',
            'auth': '/api/auth/',
            'reports': '/api/reports/',
            'organisations': '/api/organisations/',
        },
        'docs': '/docs/',
        'swagger': '/swagger/'
    })
