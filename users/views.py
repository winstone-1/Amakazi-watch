from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.logging import log_action

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', 'survivor')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        refresh = RefreshToken.for_user(user)

        log_action('register', user=user, details={'role': role})
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': getattr(user, 'role', 'survivor'),
            },
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)
                response.data['user'] = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': getattr(user, 'role', 'survivor'),
                }
                log_action('login', user=user)
            except User.DoesNotExist:
                pass
        return response

class GoogleAuthCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        access_token = request.data.get('access_token')
        user_info = request.data.get('user_info')
        
        if not access_token:
            return Response({'error': 'Access token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # If user_info not provided, fetch from Google
        if not user_info:
            try:
                import requests
                response = requests.get(
                    'https://www.googleapis.com/oauth2/v3/userinfo',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                response.raise_for_status()
                user_info = response.json()
            except requests.exceptions.RequestException as e:
                return Response({'error': f'Failed to fetch user info: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = user_info.get('email')
        name = user_info.get('name', '')
        
        if not email:
            return Response({'error': 'Email not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=name.split()[0] if name else '',
                last_name=' '.join(name.split()[1:]) if name else '',
                password=None,
                role='survivor'
            )
        
        # Generate JWT tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': getattr(user, 'role', 'survivor')
            }
        })
